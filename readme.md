Webserver slouzici pro system obrazovek v patrech na festivalu jeden svet na ohradni (jsnsgekom.cz)

# Poznamky
- current den se meni na route /change_current_day
- authentikace je udelana pomoci zahashovanyho tokenu, username neni treba
- je to hnus ale vadi to nekomu?
- /floor vzdycky posila request na hlavni server. pokud dostane odpoved, ulozi ji do promenne latest_responses. pokud nekdy server neodpovi, nacte odpoved ulozenou v latest_respones. POZOR - aby tohle fungovalo, server musi bezet jenom s jednim workerem, protoze workeri nesdileji lokalni promenne