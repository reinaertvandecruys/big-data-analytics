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

publication count:

Wanneer we gaan kijken naar de resultaten gesorteerd op publication count (PC) 
zien we dat een klein deel van de auteurs een publication count hoger dan 10 heeft. 
De auteur Leonid Libkin heeft de meeste publicatie namelijk 34. De top 5 bestaat 
uit Leonid Libkin (PC 34), Yehoshua Sagiv (PC 31), Moshe Y. Vardi (PC 30), Victor 
Vianu (PC 28) en Dan Suciu (PC 28). We zien ook dat de auteurs die bovenaanstaan 
veel publicatie hebben uitgebracht samen met andere auteurs met een hoge PC. Er 
is bijvooorbeeld niemand met een hoge PC die enkel met mensen heeft samengewerkt 
met een PC van maximum 10. Auteurs met een hoge PC hebben een relatief hoge 
pagerank, hub en authority score. Wanneer we gaan sorteren op pagerank of Authority
zien we dat het niet wilt zeggen dat een persoon de meeste publicaties heeft
dat deze ook de belangrijkste auteur is.


PageRank:

Wanneer we sorteren op pagerank zien we dat op de eerste plaats Georg Gottlob met 
een pageRank van 0.006062. Wat direct opvalt is dat Leonid Libkin, de auteur met 
de hoogste PC, bij de pagerank op de 2de plaatst komt. We kunnen hieruit concluderen
dat Georg Gottlob samen heeft gewerkt met belangrijkere auteurs dan Leonid Libkin 
en/of libkin meer publicatie op zijn eigen heeft uitgebracht. In de top 10 staat
Raghu Ramakrishnan met een pagerank van 0.004709, Raghu heeft slechts een PC van 15. 
Bij de PC ranking komt Raghu Ramakrishnan dan ook op de 19de plaats. Moshe Y. Vardi
de auteur met 30 publicaties komt pas op de 15de plaats met een pagerank van 0.003982. 

Wanneer we gaan kijken naar de laagste pageranks zien we dat er verschillende auteurs
een pagerank hebben van 0.000132. Deze auteurs hebben allemaal gemeenschappelijk dat 
ze niet samen met andere auteurs gepubliceerd hebben.


Authority:

Bij het sorteren op Authority valt ons direct op dat er 4 auteurs in de top 10 van 
hoogste authority staan met een CP van onder de 10. Dit betekend dat deze 4 personen 
hebben samen gewerkt met belangrijke auteurs die een hoge hub score hebben 
(dus naar verschillende auteurs met een hoge Authority linken). In dit geval is de Authority
score gelijk aan de hub score omdat we te maken hebben met undirected edges. 3 van deze 4 staan 
op de 4de, 5de en 6de plaats met een PC van 9 wanneer we gaan kijken naar de coauteurs
van deze auteurs zien we dat ze elkaar als coautheur hebben. Deze auteurs hebben ook nog 
Moshe Y. Vardi en Riccardo Rosati als gemeenschappelijke coauteur. Deze 3 auteurs hebben 
een hoge authority score omdat ze hebben samengewerkt met Moshe Y. Vardi. Moshe Y. Vardi heeft 
namelijk de hoogste hub score. Riccardo Rosati is van minder belang omdat deze enkel een hoge
authority score heeft omdat hij heeft samengewerkt met de 3 auteurs. Leonid Libkin (PC 34) komt 
op de 14de plaats terwijl deze 2de was bij pagerank.

We kunnen dus concluderen dat Leonid Libkin een belangrijke auteur is volgens pagerank 
maar dat bij het HITS algoritme minder belangrijk is doordat hij veel samenwerkt met 
minder belangrijke auteurs. Voor de auteur Moshe Y. Vardi geldt het tegenovergestelde. 
Yehoshua Sagiv (PC 31) zijn beide waarden ongeveer gelijk. Bij pagerank staat hij op de
4de plaats, bij Authority op de 7de en voor PC de 2de plaats.
