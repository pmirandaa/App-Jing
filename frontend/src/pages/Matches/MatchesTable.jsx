import { API_URL } from "constants";
import Table from "react-bootstrap/Table";
import moment from "moment";
import { Button } from "react-bootstrap";
import axios from "axios";
import { useAlert } from "react-alert";
import { useState } from "react";
import { Check2, InfoCircleFill, TrashFill, XLg } from "react-bootstrap-icons";
import styles from "./MatchesTable.module.css";

export default function MatchesTable({ rows, fetchData, ...props }) {
  const [isLoading, setIsLoading] = useState(false);

  const alert = useAlert();

  function requestAction(matchId, action) {
    axios
      .post(`${API_URL}/matches/${matchId}/${action}/`)
      .then((response) => {
        fetchData({ scrollToTop: false });
        alert.show("El partido ha sido cerrado");
      })
      .finally(() => {
        setIsLoading(false);
      })
      .catch((error) => {
        const error_code = error?.response?.data?.code;
        if (error_code) {
          alert.error("Este partido ya se encontraba cerrado");
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
            <td>{row.played ? <Check2 size={24} /> : <XLg/>}</td>
            <td>{row.closed ? <Check2 size={24} /> : <XLg/>}</td>
            <td className="text-center">
              <Button className={styles["action"]} variant="secondary" onClick={() => handleClickFinish(row.id)}>
                Finalizar
              </Button>
              <Button className={styles["action"]} onClick={() => handleClickFinish(row.id)}>
                <InfoCircleFill/>
              </Button>
              <Button className={styles["action"]} variant="danger" onClick={() => handleClickDelete(row.id)}><TrashFill /></Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
