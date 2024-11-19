Webserver slouzici pro system obrazovek v patrech na festivalu jeden svet na ohradni (jsnsgekom.cz)

# Poznamky
- current den se meni na route /change_current_day
- authentikace pomoci flask-login - asi overkill ale zase co jsem zejo
- /patro vzdycky posila request na hlavni server. pokud dostane odpoved, ulozi ji do promenne latest_responses. pokud nekdy server neodpovi, nacte odpoved ulozenou v latest_respones. POZOR - aby tohle fungovalo, server musi bezet jenom s jednim workerem, protoze workeri nesdileji lokalni promenne
- velikost text itemu v programu se automaticky zmensuje pokud se nevejdou
- ve floor.html k nazvu static souboru pridavam nahodny ?v argument, aby je browser necachoval
- je potreba vzdycky pouzivat jiny nazvy obrazku, jinak je browser nacachuje a bude nejakou dobu trvat nez se objevi nova verze
- po poslani requestu na /should-i-reload dostanu bud odpoved 0 nebo 1
- po poslani requestu na /reload se zmeni obsah /instance/reload.txt na 1 a spawne se thread ktery nastavi za 1 minutu content zpatky na 0
- /patro posila kazdou minutu request na /should-i-reload - pokud dostane 1 tak reloaduje