"""
심층 분석 함수 모음 — basecamp_brew_analysis.ipynb에서 임포트하여 사용.
각 함수는 집계된 DataFrame을 반환하며 출력은 노트북에서 처리한다.
"""
import pandas as pd
import numpy as np


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """월별 Revenue, Profit, 주문수, Margin%, MoM% 집계."""
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')

    agg = df.groupby('YearMonth').agg(
        Orders=('Order ID', 'count'),
        Quantity=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Cost=('Cost', 'sum'),
        Profit=('Profit', 'sum'),
    ).reset_index()

    agg['Month'] = agg['YearMonth'].dt.month
    agg['MonthName'] = agg['YearMonth'].dt.strftime('%Y-%m')
    agg['ProfitMargin_Pct'] = (agg['Profit'] / agg['Revenue'] * 100).round(1)
    # 전월 대비 매출 증감률
    agg['Revenue_MoM_Pct'] = agg['Revenue'].pct_change() * 100
    agg['Revenue_MoM_Pct'] = agg['Revenue_MoM_Pct'].round(1)

    return agg.sort_values('YearMonth').reset_index(drop=True)


def channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    """채널별 Revenue, Profit, 주문수, 객단가, 매출 비중 집계."""
    agg = df.groupby('Channel').agg(
        Orders=('Order ID', 'count'),
        Revenue=('Revenue', 'sum'),
        Cost=('Cost', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'),
    ).reset_index()

    agg['AvgOrderValue'] = (agg['Revenue'] / agg['Orders']).round(2)
    agg['ProfitMargin_Pct'] = (agg['Profit'] / agg['Revenue'] * 100).round(1)
    total_revenue = agg['Revenue'].sum()
    agg['RevenueShare_Pct'] = (agg['Revenue'] / total_revenue * 100).round(1)

    return agg.sort_values('Revenue', ascending=False).reset_index(drop=True)


def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """제품×카테고리별 Revenue, Profit, Margin 집계. Revenue 내림차순 정렬."""
    agg = df.groupby(['Product', 'Category']).agg(
        Orders=('Order ID', 'count'),
        Quantity=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Cost=('Cost', 'sum'),
        Profit=('Profit', 'sum'),
    ).reset_index()

    # 0 Revenue 방어 처리
    agg['ProfitMargin_Pct'] = np.where(
        agg['Revenue'] != 0,
        (agg['Profit'] / agg['Revenue'] * 100).round(1),
        0.0
    )

    return agg.sort_values('Revenue', ascending=False).reset_index(drop=True)


def customer_segment_summary(df_customers: pd.DataFrame) -> pd.DataFrame:
    """채널×재구매 여부별 고객수, 총 지출, 평균 지출, 평균 주문수 집계."""
    agg = df_customers.groupby(['Channel', 'Repeat Customer']).agg(
        CustomerCount=('Customer ID', 'count'),
        TotalSpend=('Total Spend', 'sum'),
        AvgSpend=('Total Spend', 'mean'),
        AvgOrders=('Total Orders', 'mean'),
    ).reset_index()

    agg['AvgSpend'] = agg['AvgSpend'].round(2)
    agg['AvgOrders'] = agg['AvgOrders'].round(1)

    return agg.sort_values(['Channel', 'Repeat Customer']).reset_index(drop=True)
