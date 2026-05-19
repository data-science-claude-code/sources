"""
데이터 프로파일링 헬퍼 — /analyze 슬래시 커맨드가 호출하는 스크립트.
Excel(.xlsx) 또는 CSV 파일을 받아 품질 리포트와 이상치를 stdout에 출력한다.
"""
import sys
import io
import warnings
from pathlib import Path

# Windows 터미널 한글 출력 보장 — CLI 직접 실행 시에만 적용 (Jupyter import 시 제외)
if __name__ == "__main__" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# 채널별 색상 팔레트 (시각화 공통)
CHANNEL_COLORS = {
    'Online': '#2E86AB',
    'Mall Kiosk': '#A23B72',
    'Downtown Shop': '#F18F01',
    "Farmer's Market": '#C73E1D'
}


def fmt_dollar(val: float) -> str:
    """금액을 $X,XXX.XX 형식으로 포맷."""
    return f"${val:,.2f}"


def load_data(filepath: str) -> dict[str, pd.DataFrame]:
    """xlsx는 시트별로, csv는 단일 DataFrame으로 로딩."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: 파일을 찾을 수 없습니다 → {filepath}", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() in (".xlsx", ".xls"):
        sheets = pd.read_excel(path, sheet_name=None, engine='openpyxl')
        return sheets
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path, encoding="utf-8-sig")
        return {"Sheet1": df}
    else:
        print(f"ERROR: 지원하지 않는 파일 형식 → {path.suffix}", file=sys.stderr)
        sys.exit(1)


def profile_data(name: str, df: pd.DataFrame) -> dict:
    """기본 데이터 품질 리포트 생성 및 출력."""
    total_rows = len(df)
    total_cols = len(df.columns)

    # 결측값 집계
    missing = df.isnull().sum()
    missing_info = [
        {"column": col, "missing_count": int(cnt),
         "missing_pct": round(cnt / total_rows * 100, 1)}
        for col, cnt in missing.items() if cnt > 0
    ]

    # 중복행
    duplicate_count = int(df.duplicated().sum())

    # 숫자 컬럼 기술 통계
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_stats = {}
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) == 0:
            continue
        numeric_stats[col] = {
            "count": int(s.count()),
            "sum": round(float(s.sum()), 2),
            "mean": round(float(s.mean()), 2),
            "median": round(float(s.median()), 2),
            "std": round(float(s.std()), 2),
            "min": round(float(s.min()), 2),
            "max": round(float(s.max()), 2),
        }

    # 날짜 컬럼 탐지 (object 타입이지만 날짜처럼 보이는 것)
    date_candidates = []
    for col in df.select_dtypes(include=["object"]).columns:
        sample = df[col].dropna().head(5).tolist()
        sample_str = " ".join(str(v) for v in sample)
        if any(c in sample_str for c in ["-", "/"]) and any(c.isdigit() for c in sample_str):
            date_candidates.append(col)

    result = {
        "sheet_name": name,
        "total_rows": total_rows,
        "total_cols": total_cols,
        "columns": list(df.columns),
        "missing_values": missing_info,
        "duplicate_rows": duplicate_count,
        "date_candidates": date_candidates,
        "numeric_stats": numeric_stats,
        "sample_data": df.head(3).to_dict(orient="records"),
    }

    # 리포트 출력
    print(f"\n[데이터 품질 리포트: {name}]")
    print(f"  총 행수: {total_rows:,}행 | 총 열수: {total_cols}개")
    print(f"  컬럼 목록: {', '.join(result['columns'])}")
    print(f"  중복 행: {duplicate_count}건")

    if missing_info:
        print("  [결측값]")
        for m in missing_info:
            print(f"    - {m['column']}: {m['missing_count']}건 ({m['missing_pct']}%)")
    else:
        print("  결측값: 없음")

    if date_candidates:
        print(f"  [날짜형 의심 컬럼]: {', '.join(date_candidates)}")

    if numeric_stats:
        print("  [수치 컬럼 통계]")
        for col, stats in numeric_stats.items():
            print(f"    {col}: 합계={stats['sum']:,.2f} | 평균={stats['mean']:,.2f} | "
                  f"최소={stats['min']:,.2f} | 최대={stats['max']:,.2f}")

    return result


def detect_anomalies(name: str, df: pd.DataFrame) -> list[dict]:
    """IQR 기반 이상치 탐지 — 수치 컬럼만 검사."""
    anomalies = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) < 10:
            continue

        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        outlier_mask = (s < lower) | (s > upper)
        outlier_count = int(outlier_mask.sum())

        if outlier_count > 0:
            outlier_vals = s[outlier_mask].tolist()
            anomalies.append({
                "sheet": name,
                "column": col,
                "outlier_count": outlier_count,
                "outlier_pct": round(outlier_count / len(s) * 100, 1),
                "lower_bound": round(float(lower), 2),
                "upper_bound": round(float(upper), 2),
                "extreme_values": sorted(outlier_vals, key=abs, reverse=True)[:5],
            })

        # 음수값 체크 (금액/수량 컬럼)
        negative_count = int((s < 0).sum())
        if negative_count > 0:
            anomalies.append({
                "sheet": name,
                "column": col,
                "issue": "음수값 발견",
                "negative_count": negative_count,
                "negative_pct": round(negative_count / len(s) * 100, 1),
            })

    return anomalies


def main(filepath: str):
    """전체 프로파일링 실행 후 리포트 출력."""
    sheets = load_data(filepath)

    all_anomalies = []
    for name, df in sheets.items():
        profile_data(name, df)
        all_anomalies.extend(detect_anomalies(name, df))

    if all_anomalies:
        print("\n" + "=" * 60)
        print("이상치 탐지 결과")
        print("=" * 60)
        for a in all_anomalies:
            if "issue" in a:
                print(f"  [{a['sheet']}] {a['column']}: {a['issue']} — {a['negative_count']}건 ({a['negative_pct']}%)")
            else:
                print(f"  [{a['sheet']}] {a['column']}: IQR 이상치 {a['outlier_count']}건 ({a['outlier_pct']}%)")
                print(f"    정상 범위: {a['lower_bound']:,.2f} ~ {a['upper_bound']:,.2f}")
    else:
        print("\n이상치: 발견되지 않음")

    print("\n프로파일링 완료.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python analysis_helper.py <데이터파일경로>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
