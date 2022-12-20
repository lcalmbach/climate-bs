HOME_INFO = """Diese App visualisiert die Witterungserscheinungen im Kanton Basel-Stadt seit 1921. Registriert wurden die Daten seit 1940 in der [Wetterstation Basel-Binningen](https://www.wetter-binningen.ch/) und während 1921-1939 im [Bernoullianum](https://de.wikipedia.org/wiki/Bernoullianum). Die Daten sind auf [OpenData Basel-Stadt](https://data.bs.ch/explore/dataset/100227/) publiziert und werden monatlich aktualisiert. Die untenstehende Tabelle zeigt alle Parameter des zuletzt abgeschlossenen Monats und vergleicht sie mit dem Mittelwert sowie Extrema aus allen historischen Daten des gleichen Monats. Unter Monats- und Jahres-Statistik können die Daten auch grafisch ausgewertet werden. 

Im Menu *Rekorde* kann für einen selektierten Parameter nach den historischen Höchst- und Tiefstwerten gesucht werden. 

Im Menu *Temperatur seit 1864* wird ein zweiter Datensatz: Temperatur Monatsmittelwerte der Station Basel/Binningen seit 1864 mittels verschiedenen Grafiktypen visualisiert. In einer 3D Darstellung kann dort die zeitliche Entwicklung mit dem globalen Trend sowie nur mit der Entwicklung auf der nördlichen Hemisphäre verglichen werden.
"""

TABLE_LEGEND = """Vergleich der Witterungserscheinungen im {} mit dem Mittelwert, Minimum und Maximum des gleichen Monats in der Vergleichsperiode. Der Vergleich erlaubt eine Abschätzung wie "normal", hoch und tief der letze Monatswert war, verglichen mit der gewählten Periode. Da über eine längere Zeit das Minimum und Maximum oft Extremwerte sind, ist eine Vergleich eines Werts mit Mittelwert ± Standard-Abweichung oft nützlicher für eine Aussage darüber, ob ein scheinbar tiefer Wert in der Tat ein ausserordentliches Ereignis darstellt oder nicht als Minimum/Maximum."""

SPIRAL_LEGEND="""
Diese 3D Darstellung ist inspiriert von [Ed Hawkins' Temperatur-Spirale](https://en.wikipedia.org/wiki/Climate_spiral). Die Differenz des Monatsmittelwert vom Referenzwert des gleichen Monats sind kreisförmig angeordnet und jedes Symbol repräsentiert einen Monat. Die Referenzperiode ist die, von Ed Hawkins gewählte, vorindustrialisierte Periode vor 1901. 

Die Temperatur-Anomalien von Basel Binningen lassen sich mit dem gesamt-globalen Trend sowie mit dem Trend auf der nördlichen Halbkugel vergleichen. Wie zu erwarten ist die Varianz in Basel/Binnigen, wo die Daten von einer einzigen Station stammen, sehr viel höher als bei den globalen Datensätzen. Bei Letzteren werden die Werte durch die vielen Stationen geglättet und beim gesamt-globalen Datensatz wird auch der Sommer/Winter-Effekt ausgeglichen. Im Gegensatz zu Hawkins Darstellung der Temperaturspirale, basiert das Color-coding nicht auf der Zeitdimension sondern auf der Temperaturanomalie: blaue Temperaturen bedeuten negative Abweichungen von den Mittelwerten der Referenzperiode, gelb-rote Töne eine positive Abweichung. Eine interessante Feststellung, die man dabei gewinnen kann ist, dass dass sich der globel kalte Winter von Januar bis März 1878 in den Daten von Basel nicht wiederfindet.

Die Grafik lässt sich drehen, verschieben und mit der Mousescroll-Taste zoomen, je nach Perspekitve lassen sich unterschiedliche Erkenntnisse gewinnen.
"""

GW_SPIRAL_LEGEND_PRE = """
Diese Daten sind erst ca. ab 1983 verfügbar, eine vorindustrielle Referenzperiode (<1901) steht damit leider nicht zur Verfügung. Für diese Daten werden daher die effektiven Monatsmittel und nicht, wie bei der Lufttemperatur (Station Basel/Binningen, sowie globale Temperatur), die Differenz zu der Referenzperiode dargestellt. Wähle eine Station oder alle Stationen und schränke bei Bedarf die dargestellten Jahre in der Navigationsleiste an.
"""

GW_SPIRAL_LEGEND_POST = """
Die Grundwassertemperatur wird in 80 Messtellen des Kantons regelmässig überwacht. Die Grundwassertemperatur ist für das Thema Klima von besonderem Interesse, da dieser Parameter träge auf Schwankungen an der Oberfläche reagiert. Trends werden geglättet und sind damit besser erkennbar als in Lufttemperatur-Daten. Die für eine, in den letzten Jahren sich beschleunigende, Erwärmung des Grundwassers ist in den meisten Stationen durch die charakteristische Trichterform gut erkennbar. Eine umfangreichere Analyse der Grundwassertemperatur findest du [hier](https://groundwater-bs.herokuapp.com/) unter Menu *Analysis/Reports* > *Temperature Trend*.
"""
