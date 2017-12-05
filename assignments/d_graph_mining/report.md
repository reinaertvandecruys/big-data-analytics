# [BDA] Verslag taak 4 - Graph Mining

- Jens Vannitsen - 1334039
- Reinaert Van de Cruys - 1334947


## Implementatie

Om de betweenness centralities te berekenen, gebruiken we de networkx.betweenness_centrality() functie. Voor iedere periode van 5 of 10 jaar bouwen we een NetworkX collaboration graph op, die we vervolgens een voor een meegeven aan de functie om de bijhorende centralities te krijgen. Om de communities te berekenen, gebruiken we community_louvain, waarna we een map opbouwen met behulp van pyplot en die tekenen via networkx.draws_pring().


## Resultaten

deel 1:

Wanneer we over een periode van 10 jaar gaan kijken zien we dat de betweenness centrality van de meest centrale schrijver afneemt van de jaren 80 t.o.v. de jaren 90.
Na deze daling neemt de betweenness centrality terug toe. Over alle jaren heen hebben we steeds nieuwe mensen in de top 5 van meest centrale auteurs, enkel Georg Gottlob 
blijft op de 4de plaats (periode 00-09 en 10-19). Wanneer we verder gaan kijken dan enkel de top 5 in de datafile we bijvoorbeeld dat Oded Shmueli die in de jaren 80 op 
de eerste plaats staat, in de jaren 90 op plaats 156 komt en de volgende periodes niet meer vermeld wordt. Dit betekent dat Oded Shmueli na de jaren 90 geen publicaties 
meer heeft uitgebracht i.v.m. PODS. In vorige opdrachten was Yehoshua Sagiv een belangrijke naam, ook bij hem zien we een 
afnamen van de betweenness centrality over de jaren heen. Hij start op de 3de plaats in de jaren 90 en springt vervolgens naar de 13 en 102de plaats om vervolgens te eindigen op
plaats 287. Dit zelfde geldt ook voor andere auteurs die in de top 5 staan van de jaren 80. We zien dat de meeste auteurs één van de volgende patronen volgt:
- In vorige periode laag beginnen in ranking en iedere periode hoger en hoger geranked worden (bijvoorbeeld Dirk Van Gucht, Qin Zhang 0001, Benny Kimelfeld, etc.).
- Hun intreden doen in het jaar dat ze in de top 5 staan en de periode/s erna terug zakken in ranking (Erik Vee, Emmanuel Waller, etc.).

Net zoals Oded Shmueli komt het bij andere auteurs ook voor dat er een bepaalde periode is waarin men niets publiceert.

╔═══╤═══════╤═══════╤═══════╤═══════╗ 
║   │ 80-89 │ 90-99 │ 00-09 │ 10-19 ║
╠═══╪═══════╪═══════╪═══════╪═══════╣
║ 1 │ 5%    │ 4.2%  │ 12.6% │ 17.3% ║
╟───┼───────┼───────┼───────┼───────╢
║ 2 │ 4.4%  │ 3.3%  │ 7.1%  │ 15.1% ║
╟───┼───────┼───────┼───────┼───────╢
║ 3 │ 4.3%  │ 3.2%  │ 6.4%  │ 13.1% ║
╟───┼───────┼───────┼───────┼───────╢
║ 4 │ 4.1%  │ 3.2%  │ 5.6%  │ 9.6%  ║
╟───┼───────┼───────┼───────┼───────╢
║ 5 │ 3.9%  │ 3.1%  │ 5.2%  │ 8.7%  ║
╚═══╧═══════╧═══════╧═══════╧═══════╝
╔═══╤═══════════════════════════╤══════════════════════╤═════════════════╤══════════════════╗
║   │ 80-89                     │ 90-99                │ 00-09           │ 10-19            ║
╠═══╪═══════════════════════════╪══════════════════════╪═════════════════╪══════════════════╣
║ 1 │ Oded Shmueli              │ Alberto O. Mendelzon │ Ronald Fagin    │ Dirk Van Gucht   ║
╟───┼───────────────────────────┼──────────────────────┼─────────────────┼──────────────────╢
║ 2 │ Raghu Ramakrishnan        │ Paris C. Kanellakis  │ Ravi Kumar 0001 │ Michael Benedikt ║
╟───┼───────────────────────────┼──────────────────────┼─────────────────┼──────────────────╢
║ 3 │ Yehoshua Sagiv            │ Tova Milo            │ Erik Vee        │ Qin Zhang 0001   ║
╟───┼───────────────────────────┼──────────────────────┼─────────────────┼──────────────────╢
║ 4 │ Christos H. Papadimitriou │ Emmanuel Waller      │ Georg Gottlob   │ Georg Gottlob    ║
╟───┼───────────────────────────┼──────────────────────┼─────────────────┼──────────────────╢
║ 5 │ Nicolas Spyratos          │ Dan Suciu            │ Alan Nash       │ Benny Kimelfeld  ║
╚═══╧═══════════════════════════╧══════════════════════╧═════════════════╧══════════════════╝

Wanneer we vervolgens gaan kijken naar een periode van 5 jaar zien we dat de betweenness centrality stijgt tot eind jaren 90, afneemt in de jaren 00-04, terug stijgt in de periode 05-09 en dan terug gaat dalen. In de periode 15-19 hebben we zelfs waardes onder de 1%. Wanneer we de 10 jaar periode vergelijken met de 5 jaar periode zien we dat 4 auteurs uit de top 5 van de jaren 80 terugkomen 
in de 2de helft van de jaren 80, namelijk Yehoshua Sagiv, Christos H. Papadimitriou, Raghu Ramakrishnan en Oded Shmueli. In de jaren 90 zien we dan weer vooral namen voorkomen uit de eerste helft 
van de jaren 90, Tova Milo, Paris C. Kanellakis en Emmanuel Waller. In de jaren 00-09 zien we dat Ronald Fagin op de eerste plaats staat. Dit is te wijten een het feit dat hij zowel in de periode 
00-04 als 05-09 in de top 5 staat, namelijk positie 2 en 1. Georg Gottlob staat zowel in periode 00-09 als periode 10-19 op plaats 4. Wanneer we dit meer in detail gaan bekijken zien we dat hij zowel in de 2de helft van periode 00-09 als in de eerste helft van periode 10-19 in de top 5 staat. In de laatste 2 periodes 00-09 en 10-19 zien we terug hetzelfde verschijnsel als in de eerste 2 periodes. Periode 00-09 bevat vooral mensen uit de 2de helft en periode 10-19 uit de eerste helft. Als laatste merken we op dat Dirk Van Gucht op de eerste plaats staat in de periode 10-19, maar dat hij niet terug te vinden is in de top 5 van 10-14 en 15-19.

╔═══╤═══════╤═══════╤═══════╤═══════╤═══════╤═══════╤═══════╤═══════╗
║   │ 80-84 │ 85-89 │ 90-94 │ 95-99 │ 00-04 │ 05-09 │ 10-14 │ 15-19 ║
╠═══╪═══════╪═══════╪═══════╪═══════╪═══════╪═══════╪═══════╪═══════╣
║ 1 │ 1.3%  │ 2.7%  │ 2.9%  │ 6.9%  │ 4.4%  │ 9.6%  │ 7.2%  │ 0.99% ║
╟───┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────╢
║ 2 │ 1%    │ 2.1%  │ 2.6%  │ 5.7%  │ 4.4%  │ 7.7%  │ 5.6%  │ 0.84% ║
╟───┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────╢
║ 3 │ 0.95% │ 2.1%  │ 2.5%  │ 4.8%  │ 2.9%  │ 7.3%  │ 5.3%  │ 0.7%  ║
╟───┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────╢
║ 4 │ 0.9%  │ 1.3%  │ 2.2%  │ 3.8%  │ 2.8%  │ 5.8%  │ 5.1%  │ 0.57% ║
╟───┼───────┼───────┼───────┼───────┼───────┼───────┼───────┼───────╢
║ 5 │ 0.85% │ 1.1%  │ 1.8%  │ 3.8%  │ 2.5%  │ 5.6%  │ 4.2%  │ 0.39% ║
╚═══╧═══════╧═══════╧═══════╧═══════╧═══════╧═══════╧═══════╧═══════╝
╔═══╤════════════════════╤═══════════════════════════╤═════════════════════╤═══════════════════════════╤═══════════════╤═════════════════════╤═════════════════════╤══════════════════╗
║   │ 80-84              │ 85-89                     │ 90-94               │ 95-99                     │ 00-04         │ 05-09               │ 10-14               │ 15-19            ║
╠═══╪════════════════════╪═══════════════════════════╪═════════════════════╪═══════════════════════════╪═══════════════╪═════════════════════╪═════════════════════╪══════════════════╣
║ 1 │ Umeshwar Dayal     │ Yehoshua Sagiv            │ Tova Milo           │ Dan Suciu                 │ Leonid Libkin │ Ronald Fagin        │ Phokion G. Kolaitis │ Dan Suciu        ║
╟───┼────────────────────┼───────────────────────────┼─────────────────────┼───────────────────────────┼───────────────┼─────────────────────┼─────────────────────┼──────────────────╢
║ 2 │ Moshe Y. Vardi     │ Christos H. Papadimitriou │ Catriel Beeri       │ Christos H. Papadimitriou │ Ronald Fagin  │ Alan Nash           │ Michael Benedikt    │ Christopher Ré   ║
╟───┼────────────────────┼───────────────────────────┼─────────────────────┼───────────────────────────┼───────────────┼─────────────────────┼─────────────────────┼──────────────────╢
║ 3 │ Ronald Fagin       │ Raghu Ramakrishnan        │ Paris C. Kanellakis │ Serge Abiteboul           │ Tova Milo     │ Ravi Kumar 0001     │ Benny Kimelfeld     │ Benny Kimelfeld  ║
╟───┼────────────────────┼───────────────────────────┼─────────────────────┼───────────────────────────┼───────────────┼─────────────────────┼─────────────────────┼──────────────────╢
║ 4 │ Marc H. Graham     │ Oded Shmueli              │ Raghu Ramakrishnan  │ Jan Van den Bussche       │ Luc Segoufin  │ Georg Gottlob       │ Juan L. Reutter     │ Frank Neven      ║
╟───┼────────────────────┼───────────────────────────┼─────────────────────┼───────────────────────────┼───────────────┼─────────────────────┼─────────────────────┼──────────────────╢
║ 5 │ Ravi Krishnamurthy │ François Bancilhon        │ Emmanuel Waller     │ H. V. Jagadish            │ Edith Cohen   │ Phokion G. Kolaitis │ Georg Gottlob       │ Hung Q. Ngo 0001 ║
╚═══╧════════════════════╧═══════════════════════════╧═════════════════════╧═══════════════════════════╧═══════════════╧═════════════════════╧═════════════════════╧══════════════════╝


deel 2: 

In de map "deel 2" kan u de 2 afbeeldingen terug vinden die we vervolgens gaan bespreken. Als we gaan kijken naar de afbeelding "zonderlabels" zien we dat we een ovaal hebben met op de rand verschillende 
kleine communities. De auteurs die in deze communiets zitten hebben een kleine betweenness centrality omdat er maar een paar andere auteurs zijn waarmee ze zijn geconnecteerd. In het midden zien we veel overlappende communities. In deze communties bevinden zich waarschijnlijk de auteurs met de hoge cbetweenness centrality score. We gaan dus inzoomen op het centrale punt en voegen labels toe om een beter beeld te krijgen over de auteurs die behoren tot deze communities. Deze visualistie wordt weergegeven op de afbeelding "metlabels". Op deze afbeelding staan verschillende belangrijke auteurs onderstreept. Dit zijn auteurs die in de top 5 staan van hoogste betweenness centrality score in de periodes 05-09, 10-14 en 15-19. Al deze auteurs bevinden zich op de rand van een communitie en hebben verschillend verbindingen met andere communities, dit is ook de reden waarom hun betweeness zo hoog is. Veel van de korste paden tussen auteurs uit 2 verschillende communities lopen door de auteurs met de hoogste betweenness centrality.




