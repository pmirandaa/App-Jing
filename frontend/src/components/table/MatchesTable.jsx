import Table from "react-bootstrap/Table";
import moment from "moment";

export default function MatchesTable({ rows, ...props }) {
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
          <th>Estado</th>
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
            <td>{row.state}</td>
            <td className="text-center">
              {/* {% if person.is_admin or person.is_organizer or person.is_sports_coordinator or person.is_coach%} */}
              <form method="POST" action="{% url 'match:start' %}">
                <div
                  className="btn-group btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  {/* {% if match.state == 'MTB' %} */}
                  <input type="hidden" name="match" value="{{ match.id }}" />
                  <button type="submit" className="btn text-center btn-info">
                    <i
                      className="fas fa-play fa-sm pr-2"
                      aria-hidden="true"
                    ></i>{" "}
                    Empezar
                  </button>
                  {/* {% else %} */}
                  <button
                    type="button"
                    className="btn text-center btn-success finish-match-btn"
                    data-match="{{ match.id}}"
                  >
                    <i
                      className="fas fa-flag-checkered fa-sm pr-2"
                      aria-hidden="true"
                    ></i>
                    Terminar
                  </button>
                  {/* {% endif %} */}
                  {/* {% if person.is_coach %} */}
                  {/* {% else %} */}
                  <button
                    type="button"
                    className="btn text-center btn-danger delete-match-btn"
                    data-toggle="modal"
                    data-target="#delete-modal"
                    data-match="{{match.id}}"
                    data-name="{{match}}"
                  >
                    <i
                      className="fas fa-trash fa-sm pr-2"
                      aria-hidden="true"
                    ></i>{" "}
                    Borrar
                  </button>
                  {/* {% endif %} */}
                </div>
              </form>
              {/* {% endif %} */}
            </td>
          </tr>
        ))}

        {/* {% endfor %} */}
      </tbody>
    </Table>
  );
}
