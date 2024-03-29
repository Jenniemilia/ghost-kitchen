Helsingin Yliopiston Tietokantasovelluksen harjoitustyö. Tavoitteena on luoda Herokussa toimiva web-sovellus, joka hyödyntää Pythonin Flask-kirjastoa sekä PostgreSQL-tietokantaa.

# ghost-kitchen

Ghost Kitchen on paikka, joka mahdollistaa useamman ravintolan toimimisen saman katon alla. Paikassa ei ole ollenkaan perinteisiä asiakaspaikkoja, vaan ruokaa valmistetaan ainoastaan toimitettavaksi. Koska useampi ravintola sijaitsee saman katon alla, pystytään ruoka valmistamaan tehokkaasti, jolloin ruokahävikin määrä pienenee huomattavasti.
Ghost Kitchenin ei myöskään tarvitse kilpailla sijainnilla, vaan tilat voidaan järjestää edullisemmalta paikalta, jolloin neliöhinnat eivät ole niin korkealla.
Kuljetuksiin hyödynnetään alalla toimivia yhteistyökumppaneita.

Sovellusta voi kokeilla Herokussa [ghost-kitchen](https://ghost-kitchen.herokuapp.com/)

Voit luoda oman käyttäjätilin tai kirjautua valmiilla tunnuksilla:

|                | Käyttäjätunnus   | Salasana  |
| -------------  |:----------------:|:---------:|
| Admin oikeudet | Päällikkö        | ElHefe    |
|   Asiakas      | Kotikokki        |  Kokki3   |


## Keskeiset toiminnot

**Etusivu** 

Rekisteröityminen - Käyttäjän on mahdollista rekisteröityä, jolloin hän pystyy tekemään ruokatilauksia sekä kirjoittamaan arvosteluita. Näin käyttäjiä kannustetaan rekisteröitymään palveluun ja siten tarjoamaan ravintoloille tarkempaa dataa käyttäjistä. Kerätyn asiakasdatan avulla ravintolat pystyvät kohdistamaan tarjouksia ja suosituksia paremmin ja tehokkaammin juuri oikealle kohderyhmälle.

Hakutoiminto - Käyttäjä voi etsiä eri kriteereillä ravintoloita, esim. Vegaani, gluteeniton jne.

TOP listaus – Etusivulla näkyy tähtiarvio perustuen käyttäjien arviointien keskiarvoon.

Suosikit - Etusivulla näkyy käyttäjän omat suosikkiravintolat.

**Ravintolan kotisivu**

Käyttäjä näkee tarkempaa tietoa ravintolasta. Täältä löytyy myös muiden asiakkaiden antamat arvostelut sekä kirjautuneena voi kirjoittaa oman arvostelun sekä lisätä ravintolan suosikikseen. Sivuilta voi myös valita annoksia ostoskoriin ja tehdä ruokatilauksen.

**Ylläpitäjä**

Omilla sivuillaan ylläpitäjä voi lisätä ravintoloita sekä niihin liittyviä hakusanoja. Hän voi myös lisätä tai poistaa annoksia. Sivuilla pystyy seuraamaan tilaushistoriaa sekä näkemään kappaleissa tilatut annokset suosituin annos ensin. Näin on helppoa reagoida jos jokin annos ei myy. Ylläpitäjällä on myös oikeus poistaa asiattomia arvosteluja.
