import Table from "react-bootstrap/Table";
import moment from "moment";

export default function MatchesTable(props) {
  let matchDate;
  let matchLocation;
  let matchSport;
  let matchTeam;
  let matchState;
  if (props.matches[0]) {
    matchDate = props.matches[0].date;
    matchLocation = props.matches[0].location.name;
    matchSport = props.matches[0].sport;
    matchTeam = props.matches[0].teams[0].team_university_short_name;
    matchState = props.matches[0].state;
  }

  return (
    <Table striped variant="light">
      <thead>
        <tr>
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
        {props.matches.map((match) => (
          <tr key={match.id}>
            <td>{moment(match.date).format("ddd DD-MM-YY")}</td>
            <td>{moment(match.date).format("HH:mm")}</td>
            <td>{match.location.name}</td>
            <td>{match.sport}</td>
            <td>
              <ul>
                {match.teams.map((team) => (
                  <li key={team.team_id}>{team.team_university_short_name}</li>
                ))}
              </ul>
            </td>
            <td>{match.state}</td>
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
