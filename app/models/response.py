from pydantic import BaseModel
from typing import Optional


class VendorInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None


class ShippingInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    vessel: Optional[str] = None
    consignee: Optional[str] = None


class TaxInfo(BaseModel):
    tax_type: Optional[str] = None
    tax_rate: Optional[float] = None
    tax_amount: Optional[float] = None


class HeaderInfo(BaseModel):
    company_name: Optional[str] = None
    invoice_number: Optional[str] = None
    gst_number: Optional[str] = None
    invoice_date: Optional[str] = None
    vendor: Optional[VendorInfo] = None
    shipping: Optional[ShippingInfo] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_info: Optional[TaxInfo] = None


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    charges: Optional[float] = None
    tax_component: Optional[float] = None
    line_total: Optional[float] = None


class InvoiceData(BaseModel):
    header: HeaderInfo
    line_items: list[LineItem]


class InvoiceResponse(BaseModel):
    status: str
    data: InvoiceData
