# Match

## Acciones base

- ### List

- ### Retrieve

- ### Create

Recibe y crea directamente todos los campos de Match, excepto los siguientes:

`closed`, `time_closed`, `state`, `winner`: Se inicializan siempre con valores por defecto. Los campos de estado de partido se manejan a través de sus propias acciones, que podrían desencadenar otros efectos en los datos. No tienen ningún efecto si se reciben.

`match_teams`: Modifica los MatchTeams correspondientes. El objeto específico a modificar se buscará entre los `match_teams` del Match, primero por `id` y luego por `team`. Si ningún elemento coincide, no se modifica ningún MatchTeam.

En lugar de `match_teams`, recibe `teams`, con una lista de `team_id`.

- ### Update

Recibe y actualiza directamente todos los campos de Match, excepto los siguientes:

`closed`, `time_closed`, `state`, `winner`: No modifica estos valores. Misma razón que Create.

`match_teams`: Modifica los MatchTeams correspondientes. El objeto específico a modificar se buscará entre los `match_teams` del Match, primero por `id` y luego por `team`. Si ningún elemento coincide, no se modifica ningún MatchTeam.

- ### Delete


## Listar

- ### Played
Retorna todos los partidos que sí están marcados como `played`

- ### Pending
Retorna todos los partidos que no están marcados como `played`

## Gestión de estado
Dado que el cambiar el estado de un partido puede desencadenar otras acciones, estas acciones se separan de Update.

- ### Start
Marca un partido como iniciado. Si el partido ya estaba cerrado, finalizado o iniciado, arroja la excepción AlreadyClosed, AlreadyFinished o AlreadyStarted, respectivamente.

- ### Finish
Marca un partido como finalizado.
Si el partido ya estaba cerrado o finalizado, arroja la excepción AlreadyClosed o AlreadyFinished, respectivamente.

- ### Close
Marca un partido como cerrado.
Si el partido ya estaba cerrado, arroja la excepción AlreadyClosed.

