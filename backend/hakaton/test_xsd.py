from .xsd import to_xsd
from .models import Type, Element


def test_to_xsd():
    schema = """
<?xml version="1.0" ?>

<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="страна проживания" ty>
    <xs:complexType>
      <xs:sequence>
        <xs:element name="country_name" type="xs:string"/>
        <xs:element name="population" type="xs:decimal"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
  
  <xs:element name="страна гражданство">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="country_name" type="xs:string"/>
        <xs:element name="population" type="xs:decimal"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
    """
    t = Type(
        name='user',
        elements=[
            Element(name='first-name', type='string'),
            Element(name='last-name', type='string'),
            Element(name='age', type='integer'),
        ]
    )
    assert to_xsd(t, 'ns') == schema
