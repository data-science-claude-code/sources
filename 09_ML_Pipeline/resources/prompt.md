피처 엔지니어링이 완료된 고객 이탈 데이터셋 customer_churn_engineered.csv가 있습니다. 타겟 변수는 'churned'입니다.

완전한 ML 파이프라인을 구축해 주세요:

1. 데이터를 학습/테스트 세트로 분할 (80/20, 계층적 샘플링 적용)
2. 전처리 파이프라인 구성:
   - 결측값 대체 (Imputation)
   - 범주형 변수 인코딩
   - 수치형 피처 스케일링
3. 다음 모델들을 학습 및 평가: 로지스틱 회귀, 랜덤 포레스트, XGBoost
4. 각 모델에 대해 다음 지표를 출력: 정확도(Accuracy), 정밀도(Precision), 재현율(Recall), F1 점수, AUC-ROC
5. 5-겹 교차 검증(5-fold Cross-Validation)으로 안정적인 성능 추정
6. 최적 모델의 하이퍼파라미터를 GridSearchCV로 튜닝
7. 최적 모델의 혼동 행렬(Confusion Matrix)과 ROC 곡선 시각화
8. 중요도 상위 10개 피처 출력
9. 최종 학습된 모델을 churn_model.pkl로 저장

어떤 모델이 가장 좋은 성능을 보이며, 그 이유는 무엇인가요?
