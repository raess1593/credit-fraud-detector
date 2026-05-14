from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    Time: float = Field(
        ...,
        description="Seconds elapsed since the first transaction",
        json_schema_extra={"example": 0.0},
    )
    Amount: float = Field(
        ...,
        description="Monetary amount of the transaction",
        json_schema_extra={"example": 149.62},
    )

    V1: float = Field(..., json_schema_extra={"example": -1.359807})
    V2: float = Field(..., json_schema_extra={"example": -0.072781})
    V3: float = Field(..., json_schema_extra={"example": 2.536347})
    V4: float = Field(..., json_schema_extra={"example": 1.378155})
    V5: float = Field(..., json_schema_extra={"example": -0.338321})
    V6: float = Field(..., json_schema_extra={"example": 0.462388})
    V7: float = Field(..., json_schema_extra={"example": 0.239599})
    V8: float = Field(..., json_schema_extra={"example": 0.098698})
    V9: float = Field(..., json_schema_extra={"example": 0.363787})
    V10: float = Field(..., json_schema_extra={"example": 0.090794})
    V11: float = Field(..., json_schema_extra={"example": -0.5516})
    V12: float = Field(..., json_schema_extra={"example": -0.617801})
    V13: float = Field(..., json_schema_extra={"example": -0.99139})
    V14: float = Field(..., json_schema_extra={"example": -0.311169})
    V15: float = Field(..., json_schema_extra={"example": 1.468177})
    V16: float = Field(..., json_schema_extra={"example": -0.470401})
    V17: float = Field(..., json_schema_extra={"example": 0.207971})
    V18: float = Field(..., json_schema_extra={"example": 0.025791})
    V19: float = Field(..., json_schema_extra={"example": 0.403993})
    V20: float = Field(..., json_schema_extra={"example": 0.251412})
    V21: float = Field(..., json_schema_extra={"example": -0.018307})
    V22: float = Field(..., json_schema_extra={"example": 0.277838})
    V23: float = Field(..., json_schema_extra={"example": -0.110474})
    V24: float = Field(..., json_schema_extra={"example": 0.066928})
    V25: float = Field(..., json_schema_extra={"example": 0.128539})
    V26: float = Field(..., json_schema_extra={"example": -0.189115})
    V27: float = Field(..., json_schema_extra={"example": 0.133558})
    V28: float = Field(..., json_schema_extra={"example": -0.021053})
