# Notes

## Structure (35 min + Q&A)

1. **Das Problem** (~5 min) -- Regulatorischer Druck, Cloud-Komfort, Angst vor Rückschritt
2. **Was macht Cloud bequem?** (~5 min) -- Cloud als Produkt, Eigenschaften, Prozesse vor Technik, 80/20
3. **Die drei Schichten** (~7 min) -- Source of Truth, Automatisierung, Pipelines (kurze technische Anker)
4. **Compliance und Nachvollziehbarkeit** (~5 min) -- ITIL, ISO, Audits, Prozesse definieren Services
5. **Produkte und Prozesse definieren** (~5 min) -- Was ist euer Produkt? Implizit -> explizit. Nicht alles, nicht sofort.
6. **Brownfield-Muster** (~5 min) -- Inventar, ein Prozess, ausweiten
7. **Fazit** (~3 min) -- Klarheit vor Technik, Rückführung als Upgrade

## Roter Faden

Souveränität ist keine Präferenz, sondern regulatorische Realität. Die
Angst vor Repatriation ist berechtigt, wenn man nur an Technik denkt. Der
Vortrag zeigt, dass Cloud-Komfort ein Produktdesign ist -- wer versteht,
woraus er besteht, kann ihn reproduzieren.

Die Reihenfolge ist: Produkte definieren, Prozesse klären, entscheiden wo
Automatisierung sich lohnt, dann (und erst dann) die Technik. Nicht alles
muss automatisiert werden, und nicht alles muss sofort automatisiert werden.

Wenn Prozesse explizit und automatisiert sind, werden Compliance und Change
Management zu Nebenprodukten statt zu separaten Aufwänden.

## Kernaussagen

- Souveränität ist regulatorisch getrieben: Data Act, NIS2, DORA, AI Act.
  Das ist kein Trend, sondern Handlungsdruck.
- Cloud-Komfort ist ein Produkt. Die Technik kam danach.
- Vor der Automatisierung: Was sind unsere Produkte? Was sind unsere Prozesse?
- 80/20: Die häufigsten Standardfälle zuerst. Sonderfälle dürfen manuell
  bleiben. Das ist eine bewusste Entscheidung, kein Versagen.
- Drei Schichten: Source of Truth, Automatisierung, Pipelines. Kurze
  technische Anker (Netbox, Ansible, CI/CD, Idempotenz, Drift Detection),
  aber als Beweis, nicht als Kerninhalt.
- Compliance als Nebenprodukt: Merge Request = Change Record, Pipeline Log =
  Ausführungsnachweis, Source of Truth = Dokumentation. ITIL Change Mgmt und
  ISO-Audits werden einfacher, nicht schwieriger.
- Prozesse definieren den Servicekatalog. Neue Services = neue Pipelines.
- Brownfield ist der Normalfall. Ein Prozess nach dem anderen.

## Bewusste Abgrenzungen

- Kein Tool-Vergleich. Netbox/Nautobot, Ansible/Nornir einmal erwähnen,
  nicht vertiefen.
- Technische Tiefe nur als Anker/Beweis, nicht als Kerninhalt. Die
  Entscheider:innen im Publikum müssen die Konzepte mitnehmen, nicht die
  Implementierung.
- Kein ,,automatisiert alles``. Explizit: manche Dinge bleiben manuell.
- Kein perfektes Greenfield-Design. Brownfield, schrittweise.

## Taktik: technische Anker

In Sektion 3 (,,Die drei Schichten``) kurz Jargon zeigen: Idempotenz, Desired
State, Drift Detection, Config Compliance, CI/CD Pipeline, Dry-Run. Nicht
erklären, nicht vertiefen -- nur zeigen, dass das echte Konzepte sind und
dass der Sprecher die Tiefe kennt. Wer es kennt, nickt; wer nicht, nimmt das
Konzept mit, nicht das Wort.

## Open questions / TODO

- Konkrete Beispiele/Anekdoten aus kommunalen Projekten vorbereiten
- Diagramm: Architektur-Überblick (Source of Truth + Automation + Pipeline)
- Diagramm: Request-Flow (ein konkreter Vorgang Ende zu Ende)
- Eventuell: Vorher/Nachher (manueller Prozess vs. automatisierter Prozess)
- Welche Regulatorik erwähnen? Data Act + NIS2 + DORA sicher, AI Act evtl.
