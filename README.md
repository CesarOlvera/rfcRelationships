# RFC Relationships

In some cases you want to check the status of a list of IETF RFCs:

- Preparation of a Request for Quotation (RfQ).
- Analysis of a Product Datasheet.
- Verification of the Requirements for IPv6 in ICT Equipment.
  -  https://www.ripe.net/publications/docs/ripe-772
  -  http://www.ipv6.unam.mx/documentos/Recomendaciones_Licitaciones-Compras-equipos-para-IPv6-UNAM-v6.pdf


This script is provided as is to help with the those checks.

From RFC 7841:

   "[<RFC relation>:<RFC number[s]>]  Some relations between RFCs in the
      series are explicitly noted in the RFC header.  For example, a new
      RFC may update one or more earlier RFCs.  Currently two
      relationships are defined: "Updates" and "Obsoletes" [RFC7322].
      Variants like "Obsoleted by" are also used (e.g, in [RFC5143]).
      Other types of relationships may be defined by the RFC Editor and
      may appear in future RFCs."
  
  
# Usage
  
python3 rfc_relationships.py [-di] [-h] [-v]

optional arguments:
    -di, --downloadIndex  Download current official RFC Index from
                          "http://www.ietf.org/download/rfc-index.txt",
                          if this option is not included, then it uses a
                          local RFC index downloaded previously.
    -h, --help            Show this help message and exit.
    -v, --version         Show program's version number and exit.


Input:  One file "my-rfc-list.txt" with the list of RFCs you want to verify.
        It has a list of RFCs specified as RFCXXXX or XXXX,
        and separated with new line (\n) or comma (,).

Output: Three files:
        - "rfc-analysis.txt"  with analysis of all RFCs with their information,
           and stating if they are "Obsoleted" or "Updated".
        - "rfc-obsoleted.txt" with the list of obsoleted RFCs.
        - "rfc-updated.txt"   with the list of updated RFCs.

 
![alt text](rfc_relationships_graph.png)
