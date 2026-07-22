from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelectorMap:
    title : str = None
    category_path : str = None
    price : str | None = None
    description : str = None
    technical_details : dict[str,str] = field(default_factory=dict)
    product_image : str = None
    custom_selectors : dict[str,str] = field(default_factory=dict)


@dataclass(frozen=True)
class SiteConfig:
    """Dataclass to store selector configuration"""
    domain : str
    url : str
    selectors : SelectorMap






