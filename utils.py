from pydantic import BaseModel, Field
from typing import List, Optional



# Function to recursively replace \n with spaces in dictionary values
def replace_newlines(obj):
    if isinstance(obj, dict):
        return {k: replace_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_newlines(i) for i in obj]
    elif isinstance(obj, str):
        return obj.replace('\n', ' ')
    else:
        return obj
    
# Function to ensure that comma-separated strings are converted to a list of objects
def ensure_single_value(obj):
    if isinstance(obj, dict):
        return {k: ensure_single_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ensure_single_value(i) for i in obj]
    elif isinstance(obj, str) and ',' in obj:
        # Split the string by commas, create a list of dicts with single key-value pairs
        return [{'name': service.strip()} for service in obj.split(',')]
    else:
        return obj

""" Customed classes
    従業員: Optional[str] = Field(..., description="従業員それともロール")
    ロール: Optional[str] = Field(..., description="役職またはジョブタイトル")
    責任: Optional[str] = Field(..., description="ロールに関連する責任")
    作業: Optional[str] = Field(..., description="実行すべきタスクや仕事")
    締切: Optional[str] = Field(..., description="タスクの締切日または期日")
    努力: Optional[float] = Field(..., description="見積もられた労力または所要時間")
"""
class Extract(BaseModel):
    """Predefine extract fields."""
  # Employee name or identifier
    class Config:
        extra = 'allow'  # Allow extra fields

class ExtractJSON(BaseModel):
    """A list of objects within the organizational structure."""
    Extract_org: List[Extract] = Field(..., description="A list of objects")


