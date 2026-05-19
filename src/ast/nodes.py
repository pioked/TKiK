from dataclasses import dataclass
from typing import List, Optional, Any

class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode]

@dataclass
class NumberNode(ASTNode):
    value: float

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BoolNode(ASTNode):
    value: bool

@dataclass
class VariableNode(ASTNode):
    name: str

@dataclass
class MatrixNode(ASTNode):
    rows: List[List[ASTNode]]

@dataclass
class BinOpNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

@dataclass
class UnaryOpNode(ASTNode):
    op: str
    expr: ASTNode

@dataclass
class AssignNode(ASTNode):
    var_name: str
    value: ASTNode

@dataclass
class PrintNode(ASTNode):
    expression: ASTNode

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    true_body: BlockNode
    false_body: Optional[BlockNode]

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: BlockNode

@dataclass
class ForNode(ASTNode):
    iterator_name: str
    start_expr: ASTNode
    end_expr: ASTNode
    step_expr: Optional[ASTNode]
    body: BlockNode

@dataclass
class DefNode(ASTNode):
    func_name: str
    params: List[str]
    body: BlockNode

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]

@dataclass
class FuncCallNode(ASTNode):
    func_name: str
    args: List[ASTNode]

@dataclass
class BreakNode(ASTNode):
    pass

@dataclass
class ContinueNode(ASTNode):
    pass