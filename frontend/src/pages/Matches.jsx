export default function Matches() {
  return (
    <div>
      <nav>
        <div class="nav nav-tabs nav-fill" id="nav-tab" role="tablist">
          <a
            class="nav-item nav-link active"
            id="nav-home-tab"
            data-toggle="tab"
            href="#nav-home"
            role="tab"
            aria-controls="nav-home"
            aria-selected="true"
          >
            Pendientes
          </a>
          <a
            class="nav-item nav-link"
            id="nav-profile-tab"
            data-toggle="tab"
            href="#nav-profile"
            role="tab"
            aria-controls="nav-profile"
            aria-selected="false"
          >
            Pasados
          </a>
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div
          class="tab-pane fade show active"
          id="nav-home"
          role="tabpanel"
          aria-labelledby="nav-home-tab"
        >
          <div class="container-fluid">
            {/* {% if person.is_admin or person.is_organizer or person.is_sports_coordinator %} */}
            <div class="row mt-3">
              <div class="col"></div>
              <div class="col-10 d-flex justify-content-end">
                {/* <button type="button" class="btn btn-light">Cargar Partidos</button> */}
                <button
                  class="btn btn-primary"
                  type="button"
                  data-toggle="modal"
                  data-target="#create-modal"
                >
                  Crear Partido
                </button>
              </div>
              <div class="col"></div>
            </div>
            {/* {% endif %} */}
            <div class="row">
              <div class="table-responsive col-md-10 offset-md-1 mt-4">
                <table
                  id="pending-matches"
                  class="table table-striped table-bordered table-hover"
                  cellspacing="0"
                  width="100%"
                >
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
                    {/* {% for match in pending %} */}
                    <tr>
                      <td>[DD-MM-Y]</td>
                      <td>[HH:mm]</td>
                      <td>[LOCATION]</td>
                      <td>[SPORT]</td>
                      <td>
                        <ul>
                          {/* {% for team_match in match.teams.all %} */}
                          <li>[UNI]</li>
                          {/* {% endfor %} */}
                        </ul>
                      </td>
                      <td>[STATE]</td>
                      <td class="text-center">
                        {/* {% if person.is_admin or person.is_organizer or person.is_sports_coordinator or person.is_coach%} */}
                        <form method="POST" action="{% url 'match:start' %}">
                          <div
                            class="btn-group btn-group-sm"
                            role="group"
                            aria-label="Basic example"
                          >
                            {/* {% if match.state == 'MTB' %} */}
                            <input
                              type="hidden"
                              name="match"
                              value="{{ match.id }}"
                            />
                            <button
                              type="submit"
                              class="btn text-center btn-info"
                            >
                              <i
                                class="fas fa-play fa-sm pr-2"
                                aria-hidden="true"
                              ></i>{" "}
                              Empezar
                            </button>
                            {/* {% else %} */}
                            <button
                              type="button"
                              class="btn text-center btn-success finish-match-btn"
                              data-match="{{ match.id}}"
                            >
                              <i
                                class="fas fa-flag-checkered fa-sm pr-2"
                                aria-hidden="true"
                              ></i>
                              Terminar
                            </button>
                            {/* {% endif %} */}
                            {/* {% if person.is_coach %} */}
                            {/* {% else %} */}
                            <button
                              type="button"
                              class="btn text-center btn-danger delete-match-btn"
                              data-toggle="modal"
                              data-target="#delete-modal"
                              data-match="{{match.id}}"
                              data-name="{{match}}"
                            >
                              <i
                                class="fas fa-trash fa-sm pr-2"
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
                    {/* {% endfor %} */}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-profile"
          role="tabpanel"
          aria-labelledby="nav-profile-tab"
        >
          <div class="container-fluid">
            <div class="table-responsive col-md-10 offset-md-1 mt-4">
              <table
                id="played-matches"
                class="table table-striped table-bordered table-hover"
                cellspacing="0"
                width="100%"
              >
                <thead>
                  <tr>
                    <th>Deporte</th>
                    <th>Participantes</th>
                    <th>Ganador</th>
                    <th>Estado</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {/* {% for match in played_open %} */}
                  <tr>
                    <td>[SPORT]</td>
                    <td>
                      <ul>
                        {/* {% for tm in match.teams.all %} */}
                        <li> [UNI] </li>
                        {/* {% endfor %} */}
                      </ul>
                    </td>
                    <td>[UNI_WIN]</td>
                    <td>[STATE]</td>
                    <td class="text-center">
                      <div
                        class="btn-group btn-group-sm"
                        role="group"
                        aria-label="Basic example"
                      >
                        {/* {% if not match.closed %} */}
                        <button
                          type="button"
                          class="btn text-center btn-warning close-match-btn"
                          data-match="{{ match.id}}"
                        >
                          <i
                            class="fas fa-key fa-sm pr-2"
                            aria-hidden="true"
                          ></i>
                          Cerrar
                        </button>
                        {/* {% for tm in match.teams.all %} */}
                        {/* {% if tm.team.coordinator.user == user %} */}
                        <button
                          type="button"
                          class="btn text-center btn-orange comment-match-btn"
                          data-match="{{ match.id}}"
                        >
                          <i class="fas fa-sm pr-2 fa-comment-dots"></i>
                          Agregar comentario
                        </button>
                        {/* {% endif %} */}
                        {/* {% endfor %} */}
                        {/* {% else %} */}
                        <button
                          type="button"
                          class="btn text-center btn-primary results-match-btn"
                          data-match="{{ match.id}}"
                        >
                          <i
                            class="fas fa-eye fa-sm pr-2"
                            aria-hidden="true"
                          ></i>
                          Ver resultados
                        </button>
                        {/* {% endif %} */}
                        <button
                          type="button"
                          class="btn text-center btn-danger delete-match-btn"
                          data-toggle="modal"
                          data-target="#delete-modal"
                          data-match="{{match.id}}"
                          data-name="{{match}}"
                        >
                          <i
                            class="fas fa-trash fa-sm pr-2"
                            aria-hidden="true"
                          ></i>{" "}
                          Borrar
                        </button>
                      </div>
                    </td>
                  </tr>
                  {/* {% endfor %} */}
                  {/* {% for match in played_closed %} */}
                  <tr>
                    <td>[SPORT]</td>
                    <td>
                      <ul>
                        {/* {% for tm in match.teams.all %} */}
                        <li> [UNI] </li>
                        {/* {% endfor %} */}
                      </ul>
                    </td>
                    <td>[UNI_WIN]</td>
                    <td>[STATE]</td>
                    <td class="text-center">
                      <div
                        class="btn-group btn-group-sm"
                        role="group"
                        aria-label="Basic example"
                      >
                        {/* {% if not match.closed %} */}
                        {/* {% if person.is_admin or person.is_organizer %} */}
                        <button
                          type="button"
                          class="btn text-center btn-warning close-match-btn"
                          data-match="{{ match.id}}"
                        >
                          <i
                            class="fas fa-key fa-sm pr-2"
                            aria-hidden="true"
                          ></i>
                          Cerrar
                        </button>
                        {/* {% endif %} */}
                        {/* {% else %} */}
                        <button
                          type="button"
                          class="btn text-center btn-primary results-match-btn"
                          data-match="{{ match.id}}"
                        >
                          <i
                            class="fas fa-eye fa-sm pr-2"
                            aria-hidden="true"
                          ></i>
                          Ver resultados
                        </button>
                        {/* {% endif %} */}
                        {/* {% if person.is_admin or person.is_organizer %} */}
                        <button
                          type="button"
                          class="btn text-center btn-danger delete-match-btn"
                          data-toggle="modal"
                          data-target="#delete-modal"
                          data-match="{{match.id}}"
                          data-name="{{match}}"
                        >
                          <i
                            class="fas fa-trash fa-sm pr-2"
                            aria-hidden="true"
                          ></i>{" "}
                          Borrar
                        </button>
                        {/* {% endif %} */}
                      </div>
                    </td>
                  </tr>
                  {/* {% endfor %} */}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
