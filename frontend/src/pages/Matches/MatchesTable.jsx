import Table from "react-bootstrap/Table";
import moment from "moment";
import { Button } from "react-bootstrap";
import axios from "axios";
import { useAlert } from "react-alert";
import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function MatchesTable({ rows, fetchData, ...props }) {
  const [isLoading, setIsLoading] = useState(false);

  const alert = useAlert();

  function requestAction(matchId, action) {
    axios
      .post(`http://localhost:8000/api/matches/${matchId}/${action}/`)
      .then((response) => {
        fetchData({ scrollToTop: false });
        alert.show(JSON.stringify(response.data));
      })
      .finally(() => {
        setIsLoading(false);
      })
      .catch((error) => {
        const error_code = error?.response?.data?.code;
        if (error_code) {
          alert.error(error.response.data.detail);
        } else {
          alert.error(error.message);
        }
      });
  }

  function handleClickStart(matchId) {
    requestAction(matchId, "start");
  }

  function handleClickFinish(matchId) {
    requestAction(matchId, "finish");
  }

  function handleClickDelete(matchId) {
    requestAction(matchId, "delete");
  }

  return (
    <Table striped variant="light" className="mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Fecha</th>
          <th>Hora</th>
          <th>Lugar</th>
          <th>Deporte</th>
          <th>Participantes</th>
          <th>Jugado</th>
          <th>Cerrado</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            <td>{row.id}</td>
            <td>{moment(row.date).format("ddd DD-MM-YY")}</td>
            <td>{moment(row.date).format("HH:mm")}</td>
            <td>{row.location.name}</td>
            <td>{row.sport.name}</td>
            <td>
              <ul>
                {row.teams.map((team) => (
                  <li key={team.team_id}>{team.team_university_short_name}</li>
                ))}
              </ul>
            </td>
            <td>{row.played ? "Sí" : "No"}</td>
            <td>{row.closed ? "Sí" : "No"}</td>
            <td className="text-center">
              <Button onClick={() => handleClickStart(row.id)}>Empezar</Button>
              <Button onClick={() => handleClickFinish(row.id)}>
                Terminar
              </Button>
              <Button onClick={() => handleClickDelete(row.id)}>Borrar</Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
