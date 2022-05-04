export default function Teams() {
  return (
    <div class="container">
      {/* {% if alert %} */}
      <div class="row mt-3">
        <div class="col"></div>
        <div class="col-10">
          <div
            class="alert alert-{{alert.type}} alert-dismissible fade show"
            role="alert"
          >
            [MESSAGE]
            <button
              type="button"
              class="close"
              data-dismiss="alert"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>
        <div class="col"></div>
      </div>
      {/* {% endif %} */}

      <div class="row my-5">
        <div class="col-md-6 col-12 pt-2">
          <h2>Lista de Equipos</h2>
        </div>
        {/* {% if person.is_admin or person.is_organizer  %} */}
        <div class="col-md-6 col-12 d-flex justify-content-end">
          <button
            class="btn btn-primary"
            type="button"
            data-toggle="modal"
            data-target="#create-modal"
          >
            Crear Equipo
          </button>
        </div>
        {/* {% endif %} */}
      </div>
      <div class="row">
        <div class="col-12">
          <table
            id="dt-teams"
            class="table table-striped table-bordered table-hover"
            cellspacing="0"
            width="100%"
          >
            <thead>
              <tr>
                <th>Deporte</th>
                <th>Universidad</th>
                <th>Género</th>
                <th>Tipo</th>
                <th>Coordinador</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {/* {% for team in teams %} */}
              <tr>
                <td>[SPORT]</td>
                <td>[UNIVERSITY]</td>
                <td>[GENDER]</td>
                <td>[SPORT_TYPE]</td>
                <td>[COORDINATOR]</td>
                <td class="text-center">
                  {/* {% if person.is_admin or person.is_organizer  %} */}
                  <div
                    class="btn-group btn-group-sm"
                    role="group"
                    aria-label="Basic example"
                  >
                    <button
                      type="button"
                      class="btn text-center btn-info edit-team-btn"
                      data-team="{{team.id}}"
                    >
                      <i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i>{" "}
                      Editar
                    </button>
                    <button
                      type="button"
                      class="btn text-center btn-danger delete-team-btn"
                      data-toggle="modal"
                      data-target="#delete-modal"
                      data-team="{{team.id}}"
                      data-name="{{team}}"
                    >
                      <i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i>{" "}
                      Borrar
                    </button>
                  </div>
                  {/* {% endif %} */}
                </td>
              </tr>
              {/* {% endfor %} */}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
