import { API_URL } from "constants";
import { UserContext } from "contexts/UserContext";
import Table from "react-bootstrap/Table";
import moment from "moment";
import { Button } from "react-bootstrap";
import axios from "axios";
import { useAlert } from "react-alert";
import { useState, useContext } from "react";
import { Check2, InfoCircleFill, TrashFill, XLg } from "react-bootstrap-icons";
import styles from "./MatchesTable.module.css";

// para implementar la tabla de administracion de usuarios, primero se seguira la misma logica que con las demas
export default function AdminTable({ rows, fetchData, ...props }) {
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useContext(UserContext);

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
          <th>ID</th>
          <th>Usuario</th>
          <th>Persona</th>
          <th>Email</th>
          <th>Roles</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {console.log(rows)}
        {rows.map((row) => (
            
          <tr key={row.id}>
            <td>{row.id}</td>
            <td>{row.username}</td>
            <td>{row.person}</td>
            <td>{row.email}</td>
            <td>
              <ul>
              {row.is_admin && <li>Admin</li>}
              {row.is_organizer && <li>Organizador</li>}
              {row.is_university_coordinator && <li>Coord. Univ.</li>}
              {row.is_sports_coordinator && <li>Coord. Deporte</li>}
              {row.is_player && <li>Jugador</li>}
              {row.is_coach && <li>Coach</li>}
              </ul>
            </td>
            <td></td>
          </tr>
        ))}

        {/* {% endfor %} */}
      </tbody>
    </Table>
  );
}