import Table from "react-bootstrap/Table";
import moment from "moment";

export default function TeamsTable({ rows, ...props }) {
  return (
    <Table striped variant="light" className="mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Apellido</th>
          <th>Nombre</th>
          <th>Universidad</th>
          <th>Roles</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            <td>{row.id}</td>
            <td>{row.last_name}</td>
            <td>{row.name}</td>
            <td>{row.university}</td>
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
