# [BDA] Verslag taak 3 - Importance of Researchers

- Jens Vannitsen - 1334039
- Reinaert Van de Cruys - 1334947


## Implementatie

Onze implementatie leest eenmalig de volledige dataset in, en onthoudt hierbij
hoe vaak iedere auteur samenwerkt met iedere andere auteur. Deze informatie
wordt gebruikt om, met behulp van het networkx package, een graaf van
samenwerkingen op te stellen, en voor iedere auteur de PageRank, hub score en
authority score te berekenen. Deze informatie wordt weggeschreven naar het
bestand authors.txt (of authors-snap.txt voor de snap dataset). Wanneer
authors(-snap).txt al bestaat, gebruikt onze implementatie dit bestand in plaats
van de volledige dataset te parsen, wat laadtijden vanaf de tweede uitvoering
volledig weg neemt.

Na alle data voor iedere auteur verzameld te hebben, worden de auteurs
gesorteerd volgens vier verschillende eigenschappen: publication count, PageRank,
hub score, en authority score. Deze gesorteerde informatie wordt weggeschreven
naar overeenkomstige bestanden in de results folder. Die bestanden kunnen dan
eenvoudig manueel vergeleken worden om conclusies over de data te vormen.


## Resultaten

...
