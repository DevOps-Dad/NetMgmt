awk '/VLAN31/ { start = 1; continue } /VLAN/ { start = 0; continue } start == 1  && /[Ee]rror|failed|warning/ { print pline; print } { pline = $0 }' FALC-ECFL2-02
