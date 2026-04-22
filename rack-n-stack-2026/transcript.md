hallo, ich bin veit heller von port zero und cyberwitchery lab und heute möchte
ich über netzwerkautomatisierung, souveränität, technik, und prozesse sprechen.

bevor wir beginnen, möchte ich euch allen geschlossen das du anbieten. falls
euch das nicht liegt, fühlt euch bitte von mir gesiezt, mir fällt es allerdings
einfacher, bei einer form zu bleiben.

ganz kurz zu mir, um diesen vortrag etwas einzuordnen: ich komme aus der
software-entwicklung, bin in den meisten projekten irgendwo zwischen
programmierer, team lead, und projektleitung verankert, und habe vor ca. 13
jahren damit begonnen, internet service providern, data-center-betreibern,
internet exchanges und ähnlichen unternehmen dabei zu helfen, prozesse
und netze zu digitalisieren und automatisieren. gleichzeitig bin ich auch viel
in startups unterwegs und helfe investoren bei der technischen due diligence.
ein breites feld also, aber überraschend viele parallelen.

worüber möchte ich heute sprechen? ich muss noch ein kleines geständnis machen,
bevor wir anfangen: Ich habe den Abstract vor einigen Monaten geschrieben. Damals
dachte ich, ich erzähle euch hauptsächlich, wie man DCIM, Automatisierung und
Pipelines zusammenbaut. Wir stöpseln ein bisschen Entitäten in Netzwerkconfigs,
mache ich ja auch schon ziemlich lange. Das werde ich auch zeigen, keine Frage.
Aber ich habe in den letzten Monaten gemerkt, dass das der einfache Teil ist, und
Projekte, die ich betreue oder von denen ich höre, trotzdem manchmal scheitern.
Warum, und was wir stattdessen tun sollten, zumindest aus meiner Perspektive, ist
der eigentliche Schwerpunkt heute.

wir sprechen heute viel über souveränität, und ich möchte ein bisschen dabei
helfen, den tatsächlichen prozess etwas greifbarer zu machen.

---

lasst uns bei "dem problem" anfangen. oder eben dort, wo es immer anfängt: der
entscheidung.

---

warum wir zurück in’s eigene rack wollen, hat viele verschiedene
gründe, technisch, politisch, finanziell, oder eben, wie es im moment in unser
aller köpfe herumgeistert, regulatorisch.

---

und damit verlassen wir eventuell komfort, den wir gewöhnt sind. hyperscaler
zeichnen sich vor allem dadurch aus, dass sie mir nicht im weg stehen. ich
kann schnell, programmatisch, und reproduzierbar services und produkte
hochziehen, und ich kann schnell den support erreichen, gerade wenn ich einer
der eher größeren kunden bin. zugegebenermaßen nicht immer ganz einfach, wenn
ich eher wenig geld bei den amazons dieser welt lasse, aber wenn die alternative
eine interne it ist, oftmals trotzdem nicht schlecht.

---

und dann kommt die angst. ich will einen service aufbauen, ich brauche eine neue
virtuelle maschine oder ich muss das netzwerk anpassen, und dann gibt’s
plötzlich formulare und ich warte eine woche auf bereitstellung. hatten wir
früher, und gibt’s tatsächlich auch heute noch in vielen firmen. dass uns dann
souveränitätsprojekte um die ohren fliegen, ist ja kein wunder.

---

und ich würde das framing hier gerne verschieben. ich mache das mit der
automatisierung jetzt schon eine gute dekade. es gibt genug tools und technische
lösungen für jeden teil dieser reise. und trotzdem sind diese projekte oft
langwierig, auch manchmal schwierig, und fühlen sich nach echter kraftarbeit an.
warum?

aber bevor ich das kläre, sollte ich vielleicht meine zugegebenermaßen steile
these, dass die technik gelöst ist, erst einmal untermauern.

---

ich bin tatsächlich der meinung, dass die technik das einfache problem ist.

---

wir wissen wie man automatisierungs-pipelines baut. das macht unsere community
seit jahren und jahrzehnten, und es gibt von der variante "wir stöpseln ein paar
open source tools zusammen" bis zu "wir haben unser eigenes system gebaut, vom
ticket bis zur gerätekonfiguration" für alles fallstudien, vieles öffentlich.

ich leite euch kurz durch, um kurz zu skizzieren, wie das aussehen könnte.

---

wir fangen mit unserer architektur an. wir haben ein paar systeme, da kommen
daten rein. das kann ein internes ticket-system sein, das kann ein kundenportal
sein, oder eine app, die die techniker intern verwenden. das läuft dann,
hoffentlich, in einer source of truth zusammen (ich bin mir sicher, viele von
euch haben zwei, drei oder 5 von diesen sources of truth, aber das ist ja
lösbar), dann passiert auf basis dieser source of truth automatisierung und
dinge passieren. so einfach ist es auf einer hohen ebene tatsächlich.

---

beim thema netzwerkautomatisierung ist unsere source of truth meistens ein dcim
(data center infrastructure management) oder ipam (ip address management) system
oder eben beides. darin modelliere ich sowohl physisch greifbare dinge wie
standorte, geräte, und soweiter, als auch logische dinge wie ip-bereiche und
vlans. idealerweise kann ich sogar höherwertige dinge für mein geschäft
modellieren, zum beispiel mandanten, services, oder produkte.

das gibt es in open source und enterprise-variante zum beispiel von netbox,
nautobot, infrahub, racktables, fnt command, etc. etc. kann man sich einkaufen.

---

dann kommt unsere automatisierungsschicht. viele techniker kennen hier zum
beispiel ansible. ich baue mir kommandos zusammen, die ich dann auf geräte
loslassen kann, und dann wird mir eine konfiguration gebaut. im besten fall ist
das ganze compliant, idempotent, und hat ein paar checks eingebaut, damit ich
mein netzwerk nicht mit einer fehlkonfiguration kollabieren lasse. das muss
natürlich auf jeder ebene stattfinden, also auch schon im ipam und auch in der
pipeline, aber die automatisierung als ausführende schicht ist da ganz wichtig.

---

und dann haben wir pipelines, in meinem diagramm verwirrenderweise ganz am ende.
das wichtige ist, dass mich das ganze komplexere logische zusammenhänge
modellieren lässt. das kann man zum beispiel durch ci-pipelines lösen, also so
etwas wie gitlab, was manchen leuten vielleicht ein begriff ist, oder eben durch
andere tools.

das kann dann am ende so aussehen: ich lege einen neuen switch in netbox an,
das eröffnet einen merge request in einem gitlab-repo, in dem ein inventar aller
meiner geräte liegt. da läuft dann eine ansible-pipeline drüber, entdeckt das
neue gerät, rollt in einem lab oder einer virtualisierten umgebung aus, und
durch approval durch einen kollegen und ein merge wird das ganze dann in meiner
topologie ausgerollt. nur so als beispiel.

---

wie das ganze in einer fallstudie aussehen könnte, habe ich zum beispiel mal auf
der denog im jahre 2019 zusammen mit meinem kollegen christian dieckhoff
erklärt. wir haben damals bei der WOBCOM eine automatisierungs-pipeline gebaut,
und das hat viel spaß gemacht. seitdem hat sich nochmal einiges getan und die
dinge sind noch einfacher, aber den vortrag lasse ich trotzdem hier, um ein
bisschen auf die praxis zu verweisen.

---

so, und nun habe ich die praxis abgegrast, aber wir haben immer noch nicht
geklärt, warum viele projekte nicht funktionieren.

---

und leider ist es oftmals so, dass die technik eben nur ein teil des systems
ist. viel wichtiger sind die prozesse darum, die workflows. reine
infrastruktur-anbieter haben es da einfacher, weil die produkte und services vor
allem technisch sind. viele andere firmen haben diesen luxus nicht.

---

und dann automatisiert die it trotzdem in ihrem silo, und automatisiert vor
allem technische prozesse. größere zusammenhänge wie "dieses produkt braucht
folgende netzwerkservices" oder "bei diesem prozess entstehen die folgenden
schritte" werden nicht abgebildet. stattdessen wird der teil, wo das gerät
konfiguriert wird, automatisiert, und alles was darüber liegt, muss sich
irgendwo darum formieren.

---

und dann bauen wir tooling, dass die prozesse vielleicht gar nicht abbilden
kann, weil wir fundamental auf der falschen abstraktionsebene denken. ist ja
auch ganz natürlich, wir sind techniker.

als kleine anekdote, ich war vor einiger zeit in einem projekt involviert, in
dem die techniker gar nicht wussten, was für services ihre router und switches
dann am ende eigentlich anbieten. klar können wir dann die infrastruktur
automatisieren, aber da hört es dann leider auch auf, wenn ich nicht weiß, was
auf meiner topologie überhaupt so passiert.

---

wir haben am ende keine anbindung an’s kerngeschäft, und das
automatisierungsprojekt bleibt im netzwerk stecken. und das it-team wird im
besten fall vielleicht sogar ein bisschen oder sogar signifikant viel
produktiver, aber sonst niemand.

---

was ich stattdessen vorschlage, ist dass der datenfluss den produkten,
prozessen, services, workflows folgen muss.

---

das wovor wir am anfang als angst gesprochen haben, dieser komfort-verlust, das
ist vor allem ein produktdesign-problem. technisch sieht das ganze im backend
vielleicht genau gleich aus, aber das eine verstehen die nutzer, das andere
nicht.

---

und wie sehen diese eigenschaften zum beispiel aus? eigentlich genau so, wie ich
es auf einer der ersten folien schon einmal angesprochen habe: die services und
produkte müssen direkt abgebildet sein. self service muss möglich sein. es muss
reproduzierbar und nachvollziehbar sein. und ich muss wissen, wer verantwortlich
und wer mein ansprechpartner ist. alles lösbare probleme.

---

und zum produkt-denken gehört dann eben, dass man nicht über vlans und
hypervisor-regeln nachdenkt, sondern über mandantennetze, oder skalierbare
services für die deployments der software-teams, oder sogar das onboarding neuer
mitarbeiter in der marketing-abteilung. das ist zugegebenermaßen dann schon
nicht mehr netzwerkautomatisierung, aber das sind alles automatisierbare
prozesse, die zeit sparen, aber das infrastruktur-team so peu a peu weniger und
weniger betreffen.

---

also muss ich mir mindestens diese drei fragen stellen, bevor ich automatisiere:
- was sind unsere produkte und services? hoffentlich kann ich das beantworten.
- was sind die prozesse dahinter? schon schwerer, aber oft trotzdem machbar.
- und: wo lohnt sich automatisierung, wo nicht? das sollte man vor allem
  datengetrieben angehen und nicht über befindlichkeiten. wenn ich mit einer
  automatisierung jedem sales-mitarbeiter eine stunde pro woche spare, ist das
  einfach wichtiger, als wenn ich meinen nervigsten prozess automatisiere, der
  mich aber nur zehn minuten im monat kostet.

---

die reise ist also eine prozessuale. viele prozesse sind sicher implizit. das
schöne ist, dass prozesse explizit machen schon intrinsisch wertvoll für’s
geschäft ist, und dann habe ich noch gar nicht damit angefangen, zu
automatisieren. und dann, sobald ich die prozesse auf dem papier habe, kann ich
viel besser entscheiden, wo sich das anpacken lohnt.

oder, um es mit den worten von thorsten dirks, dem ehemaligen
vorstandsvorsitzenden von telefonica deutschland auszudrücken (dieses zitat
schwirrt mir schon fast zehn jahre im kopf herum):

---

"wenn sie einen scheiß prozess digitalisieren, haben sie einen scheiß digitalen
prozess." lass ich einfach mal so stehen.

---

und wenn ich dann meine prozesse habe, dann kann ich mir gedanken dazu machen,
wo sich automatisieren lohnt. wie häufig packe ich hier an? wie oft geht es
schief? und ist es reproduzierbar oder immer ein bisschen anders.

---

natürlich will ich nicht alles sofort anpacken. das schöne ist, dass ich das
auch nicht muss. ich würde vorschlagen, dass man mit einer handvoll prozesse
beginnt, im besten fall dinge, die dem geschäft helfen, damit wir am ende nicht
wieder bei einem spaßprojekt der it landen.

ich würde auch davon abraten sofort alle sonderfälle abzubilden. klar, gedanken
drum machen sollte ich mir sofort, einfach um einschätzen zu können, ob das
design am ende für alle fälle sinn macht. aber ich muss es nicht sofort
abbilden.

---

und dann kommen wir am ende zu einem projekt, dass hoffentlich unser geschäft
gut abbildet, nur eben digital. und das wäre doch mal was, oder?

---

das schöne für die cisos und leute unter euch, die sich regelmäßig den auditoren
stellen müssen ist, dass compliance hier einfach rausfällt. auditoren lieben
aufgeschriebene prozesse, und wenn die dann auch noch automatisiert und
nachvollziehbar sind, dann sind viele sicher schon um einiges zufriedener.

---

man kann hier ganz gut von einem zum anderen brücken schlagen. merge requests
werden change records. positive request reviews werden approvals. die
pipeline-logs dienen als ausführungsnachweis, und über allem schwebt unsere
source of truth als dokumentation, die tatsächlich aktuell ist und das abbildet,
was das system heute kann. unglaublich!

---

gut für audits. will jeder auditor in jedem audit sehen. und ich muss mir keine
oder nur noch wenig gedanken drum machen.

---

und die doku ist einfach da, weil ich sie als basis meiner automatisierung
nutze. ist einfach notwendigerweise immer aktuell, außer meine pipeline ist
kaputt. (und ich wünsche euch, dass die pipeline nicht gerade kaputt ist, wenn
der auditor im haus ist)

---

bevor ich zum fazit komme und euch in den abend entlasse, möchte ich noch eine
letzte sache explizit ansprechen. ich spreche nicht nur von
greenfield-neu-entwicklungen, wo ich ohnehin alles umwerfen kann.

---

jede lösung, die ernst genommen werden will, muss mit altlasten umgehen können.
dass dinge migriert und angepasst werden müssen, ist normal. sollte es
jedenfalls sein.

lasst uns mal kurz den prozess beleuchten, einfach damit ihr das auch mal
gesehen habt.

---

zuallererst muss ich mein inventar einführen und ein datenmodell finden. das
muss erstmal nicht perfekt sein, und wird es auch nicht. aber es schafft sofort
schon mehrwert, weil die systeme plötzlich dokumentiert sind.

kurzer zwischenhinweis in eigener sache an die kollegen mit einem oder mehreren
altsystemen. ich habe für cyberwitchery lab ein open source tool namens alembic
geschrieben, das daten von verschiedenen dcims in andere migrieren kann. ihr
könnt darin sogar mappings etc. schreiben. das ist für die techniker unter euch,
wenn euch das interessiert, sprecht mich ruhig später an, dann zeige ich euch
das mal. wie gesagt, open source, also kein marketing oder so.

---

zurück zur brownfield-migrierung. wir waren bei schritt zwei. wir haben ein
inventar, und bauen so langsam unsere pipeline auf. dann können wir schon einmal
mit einem prozess anfangen, um das zu testen. bestenfalls etwas, was relativ
viel Return on Investment bringt. Es gibt in den meisten Firmen Prozesse, die
man schnell automatisieren kann, und die trotzdem eine nennenswerte
Zeitersparnis bringen. Darauf kann man sich fokussieren, dann hat man den
Beweis, dass es funktioniert, und man baut gleich Vertrauen auf.

---

Im dritten Schritt machen wir das Ganze nochmal, und dann nochmal und so weiter.
Vor allem am Anfang muss man immer noch viel anpassen, und viele Altsysteme
erstmals anbinden. Das gibt sich mit der Zeit, und dann wächst das Modell.

---

Und damit sind wir auch schon am Ende. Lasst uns das Ganze mal resümieren.

---

Ich bin der Meinung, dass die technischen Probleme größtenteils gelöst sind.
Prozesse sind das Hauptproblem. hoffentlich habe ich euch meinen standpunkt
zumindest näherbringen können, ob es nun überzeugt hat oder nicht.

---

Und, ich bin der Meinung, dass ich das für mich nutzen kann. Ich kann meine
Firma intern prozessual besser machen, und gleichzeitig eine souveräne
Rückführung durchführen. Klingt eigentlich zu schön um wahr zu sein, und ist nie
einfach, aber immer möglich.

---

Danke.
