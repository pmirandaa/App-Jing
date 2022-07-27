import Table from "react-bootstrap/Table";
import moment from "moment";

export default function TeamsTable({ rows, ...props }) {
  return (
    <Table striped variant="light" className="mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Deporte</th>
          <th>Institución</th>
          <th>Género</th>
          <th>Tipo</th>
          <th>Coordinador/a</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {rows.map((team) => (
          <tr key={team.id}>
            <td>{team.id}</td>
            <td>{team.sport}</td>
            <td>{team.university}</td>
            <td>{team.sport?.gender}</td>
            <td>{team.sport?.type}</td>
            <td>{team.coordinator}</td>
            <td></td>
          </tr>
        ))}

        {/* {% endfor %} */}
      </tbody>
    </Table>
  );
}
