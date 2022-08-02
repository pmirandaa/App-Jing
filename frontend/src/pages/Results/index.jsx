import axios from "axios";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import { TransitionGroup, SwitchTransition, CSSTransition } from "react-transition-group";
import { Container, Form, Table } from "react-bootstrap";
import Select from "react-select";
import { sleeper } from "utils";

export default function Results() {
  const { event } = useContext(EventContext);
  const [sportOptions, setSportOptions] = useState([]);
  const [selectedSport, setSelectedSport] = useState(0);
  const [standings, setStandings] = useState([]);

  function handleSelect(option, action) {
    setSelectedSport(option);
    retrieveStandings(option.value);
  }

  function retrieveStandings(sport) {
    let standings = [
      { team: "Equipo 1", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 2", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 3", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 4", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 5", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 6", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 7", points: Math.floor(Math.random() * 2000) + 1 },
      { team: "Equipo 8", points: Math.floor(Math.random() * 2000) + 1 },
    ];

    standings.sort((a, b) => b.points - a.points);
    for (let i = 0; i < standings.length; i++) {
      standings[i].pos = i + 1;
    }

    setStandings(standings);
  }

  useEffect(() => {
    if (!event) return;
    const fetch = axios
      .get(`http://localhost:8000/api/sports/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        console.log(response.data);
        const options = [{ value: "0", label: "Resultados generales", data: {} }];
        const res =
          response.data?.map((spo) => ({ value: spo.id, label: spo.name, data: spo })) ??
          [];
        setSportOptions(options.concat(res));
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  return (
    <Container style={{ padding: "16px" }}>
      <h1>Resultados</h1>
      <h4>{event?.name}</h4>

      <Form.Label htmlFor="sport">Deporte</Form.Label>
      <Select
        name="sport"
        inputId="sport"
        options={sportOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={selectedSport}
      />

      <SwitchTransition>
        <CSSTransition
          key={selectedSport.value}
          classNames="fade"
          timeout={200}
        >
          <Table striped bordered hover className="mt-5">
            <tbody>
              {standings.map((standing) => (
                <tr key={standing.pos}>
                  <td>{standing.pos}</td>
                  <td>{standing.team}</td>
                  <td>{standing.points}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CSSTransition>
      </SwitchTransition>
    </Container>
  );
}
