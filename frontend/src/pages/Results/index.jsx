import axios from "axios";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import { SwitchTransition, CSSTransition } from "react-transition-group";
import { Container, Form, Spinner, Table } from "react-bootstrap";
import Select from "react-select";
import { sleeper } from "utils";
import clsx from "clsx";
import styles from "./Results.module.scss";

import _ from "lodash";
import {
  Award,
  AwardFill,
  Check2,
  Hash,
  Trophy,
  TrophyFill,
  XLg,
} from "react-bootstrap-icons";

export default function Results() {
  const { event } = useContext(EventContext);
  const [sportsData, setSportsData] = useState([]);
  const [universitiesData, setUniversitiesData] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);
  const [standings, setStandings] = useState([]);
  const [transitionKey, setTransitionKey] = useState(0);
  const [mode, setMode] = useState("event");
  const [isLoading, setIsLoading] = useState(false);

  function handleSelect(option, action) {
    if (option.value > 0) {
      retrieveStandings(option.value);
    } else {
      retrieveEvent();
    }
  }

  function retrieveEvent() {
    setIsLoading(true);
    axios
      .get(`http://localhost:8000/api/placements/event/calculate/${event.id}/`)
      .then(sleeper(500))
      .then(({ data }) => {
        console.log(data);
        setTransitionKey(transitionKey + 1);
        setMode("event");
        setStandings(data.event_placements);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }

  function retrieveStandings(sport) {
    setIsLoading(true);
    axios
      .get(
        `http://localhost:8000/api/placements/sport/calculate/${sport}/?event=${event.id}`
      )
      .then(sleeper(500))
      .then((response) => {
        console.log(response.data);
        const res =
          response.data?.results?.map((stnd) =>
            _.pick(stnd, [
              "place",
              "university",
              "wins",
              "score",
              "participated",
              "points",
              "matches",
              "attended",
            ])
          ) ?? [];
        res.sort((a, b) => a.place - a.place);
        setTransitionKey((prev) => prev + 1);
        setMode("sport");
        setStandings(res);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setIsLoading(false);
      });

    setStandings(standings);
  }

  function getPlaceIcon(place) {
    switch (place) {
      case 1:
        return <TrophyFill />;
      case 2:
      case 3:
        return <AwardFill />;
    }
    return <Hash />;
  }

  useEffect(() => {
    if (!event) return;
    setIsLoading(true);
    axios
      .get(`http://localhost:8000/api/sports/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        const options = [
          { value: "0", label: "Resultados generales", data: {} },
        ];
        const res =
          response.data?.map((spo) => ({
            value: spo.id,
            label: spo.name,
            data: spo,
          })) ?? [];
        setSportOptions(options.concat(res));
        setSportsData(response.data);
      })
      .finally(() => {
        setIsLoading(false);
      });

    axios
      .get(`http://localhost:8000/api/universities/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        setUniversitiesData(response.data);
      });
  }, [event]);

  return (
    <Container style={{ padding: "16px" }}>
      <h1 className="d-inline">Resultados</h1>
      <SwitchTransition>
        <CSSTransition key={isLoading} classNames="fade" timeout={200}>
          {isLoading ? (
            <Spinner animation="border" variant="secondary" className="ms-3" />
          ) : (
            <></>
          )}
        </CSSTransition>
      </SwitchTransition>
      <h4>{event?.name}</h4>
      <Form.Label htmlFor="sport">Deporte</Form.Label>
      <Select
        name="sport"
        inputId="sport"
        options={sportOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
      />
      <SwitchTransition>
        <CSSTransition key={transitionKey} classNames="fade" timeout={200}>
          <Table bordered hover variant="light" className="mt-5">
            {mode === "event" && (
              <>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Universidad</th>
                    <th>Puntos</th>
                  </tr>
                </thead>
                <tbody>
                  {standings.map((standing) => (
                    <tr
                      key={`stnd-univ-${standing.university}`}
                      className={clsx({
                        [styles["row-standing"]]: true,
                        [styles["row-standing-1st"]]: standing.place === 1,
                        [styles["row-standing-2nd"]]: standing.place === 2,
                        [styles["row-standing-3rd"]]: standing.place === 3,
                      })}
                    >
                      <td className={styles["cell-place"]}>{getPlaceIcon(standing.place)} {standing.place}</td>
                      <td className={styles["cell-name"]}>
                        {
                          universitiesData.find(
                            (univ) => univ.id === standing.university
                          )?.name
                        }
                      </td>
                      <td>{standing.points}</td>
                    </tr>
                  ))}
                </tbody>
              </>
            )}
            {mode === "sport" && (
              <>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Universidad</th>
                    <th>Victorias</th>
                    <th>Marcador</th>
                    <th>Participa</th>
                    <th>Puntos</th>
                    <th>Partidos</th>
                    <th>Jugados</th>
                  </tr>
                </thead>
                <tbody>
                  {standings.map((standing) => (
                    <tr
                      key={`stnd-univ-${standing.university}`}
                      className={clsx({
                        [styles["row-standing"]]: true,
                        [styles["row-standing-forfeit"]]:
                          !standing.participated,
                        [styles["row-standing-1st"]]: standing.place === 1,
                        [styles["row-standing-2nd"]]: standing.place === 2,
                        [styles["row-standing-3rd"]]: standing.place === 3,
                      })}
                    >
                      <td className={styles["cell-place"]}>
                        {getPlaceIcon(standing.place)} {standing.place}
                      </td>
                      <td className={styles["cell-name"]}>
                        {
                          universitiesData.find(
                            (univ) => univ.id === standing.university
                          )?.name
                        }
                      </td>
                      <td>{standing.wins}</td>
                      <td>{standing.score}</td>
                      <td>
                        {standing.participated ? (
                          <Check2 className="text-success" size={24} />
                        ) : (
                          <XLg className="text-danger" />
                        )}
                      </td>
                      <td>{standing.points}</td>
                      <td>{standing.matches}</td>
                      <td>{standing.attended}</td>
                    </tr>
                  ))}
                </tbody>
              </>
            )}
          </Table>
        </CSSTransition>
      </SwitchTransition>
    </Container>
  );
}
