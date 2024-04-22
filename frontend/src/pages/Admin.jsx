import axios from "axios";
import { API_URL } from "constants";
import { sleeper } from "utils";
import { useState, useEffect, useContext, useRef } from "react";
import { UserContext } from "contexts/UserContext";

export default function Admin() {


	//hacer funcion que traiga los datos de 
	const fetchInit = async () =>{
		//setIsLoading(true);
  
		const response = await axios.get(`${API_URL}/events/?current=True`);
	}


    return (
      <div>
        <nav>
	<div class="nav nav-tabs nav-fill" id="nav-tab" role="tablist">
		{/* {% if person.is_admin %} */}
			<a class="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab"
				aria-controls="nav-home" aria-selected="true">Usuarios</a>
		{/* {% endif %} */}
		<a class="nav-item nav-link {% if person.is_organizer %}active{% endif %}" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab"
			aria-controls="nav-profile" aria-selected="false">Deportes</a>
		{/* {% if person.is_admin %} */}
			<a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-contact" role="tab"
				aria-controls="nav-contact" aria-selected="false">Eventos</a>
			<a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-locations" role="tab"
				aria-controls="nav-contact" aria-selected="false">Lugares</a>
			<a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-universities" role="tab"
				aria-controls="nav-contact" aria-selected="false">Organizaciones</a>
		{/* {% endif %} */}
	</div>
</nav>
{/* {% if alert %} */}
<div class="row mt-3">
	<div class="col"></div>
	<div class="col-10">

		<div class="alert alert-{{alert.type}} alert-dismissible fade show" role="alert">
			[MESSAGE]
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
		</div>
	</div>
	<div class="col"></div>
</div>
{/* {% endif %} */}
<div class="tab-content" id="nav-tabContent">
	{/* {% if person.is_admin %} */}
	<div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-10 col-12 mt-5 offset-md-1">
					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create-modal"
						id="create-user-btn">
						Nuevo Usuario
					</button>
				</div>
			</div>
			<div class="row">
				<div class="table-responsive col-md-10 offset-md-1 mt-4">
					<table id="dt-users" class="table table-striped table-bordered table-hover" cellspacing="0"
						width="100%">
						<thead>
							<tr>
								<th>RUT</th>
								<th>Nombre</th>
								<th>Email</th>
								<th>Organización</th>
								<th>Roles</th>
								<th>Acciones</th>
							</tr>
						</thead>
						<tbody>
							{/* {% for person in people %} */}
							<tr>
								<td>[RUT]</td>
								<td>[NAME]</td>
								<td>[EMAIL]</td>
								<td>[UNI]</td>
								<td>
									<ul>
										{/* {% if person.is_admin %} */}
                      <li>Administrador</li>
                    {/* {% endif %} */}
										{/* {% if person.is_organizer %} */}
                      <li>Organizador</li>
                    {/* {% endif %} */}
										{/* {% if person.is_university_coordinator %} */}
                      <li>Coord. Organización</li>
                    {/* {% endif %} */}
										{/* {% if person.is_sports_coordinator %} */}
                      <li>Coord. Deporte</li>
                    {/* {% endif %} */}
										{/* {% if person.is_player %} */}
                      <li>Deportista</li>
                    {/* {% endif %} */}
										{/* {% if person.is_coach %} */}
                      <li>Entrenador</li>
                    {/* {% endif %} */}
									</ul>
								</td>
								<td class="text-center">
									<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
										<button type="button" class="btn text-center btn-info edit-user-btn"
											data-user="{{ person.id }}">
											<i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i> Editar
										</button>
										<button type="button" class="btn text-center btn-danger delete-user-btn"
											data-toggle="modal" data-target="#delete-modal" data-user="{{person.id}}"
											data-user-name="{{person.name}}">
											<i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i> Borrar
										</button>
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
	{/* {% endif %} */}
	<div class="tab-pane fade {% if person.is_organizer %}show active{% endif %}" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
		<div class="container-fluid">
			{/* {% if person.is_admin %} */}
			<div class="row">
				<div class="col-md-10 col-12 mt-5 offset-md-1">
					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create-modal"
						id="create-sport-btn">
						Nuevo Deporte
					</button>
				</div>
			</div>
			{/* {% endif %} */}
			<div class="row">
				<div class="table-responsive col-md-10 offset-md-1 mt-4">
					<table id="dt-sports" class="table table-striped table-bordered table-hover" cellspacing="0"
						width="100%">
						<thead>
							<tr>
								<th>Nombre</th>
								<th>Género</th>
								<th>Tipo</th>
								<th>Coordinador</th>
								<th>Acciones</th>
							</tr>
						</thead>
						<tbody>
							{/* {% for sport in sports %} */}
							<tr>
								<td>[SPORT]</td>
								<td>[GENDER]</td>
								<td>[TYPE]</td>
								<td>[COORDINATOR]</td>
								<td class="text-center">
									<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
										{/* {% if person.is_admin %} */}
										<button type="button" class="btn text-center btn-info edit-sport-btn"
											data-sport="{{sport.id}}">
											<i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i> Editar
										</button>
										<button type="button" class="btn text-center btn-danger delete-sport-btn"
											data-toggle="modal" data-target="#delete-modal" data-sport="{{ sport.id }}"
											data-name="">
											<i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i> Borrar
										</button>
										{/* {% endif %} */}
										{/* {% if sport.closed %} */}
											El campeonato se ha cerrado
										{/* {% else %} */}
											<button type="button" class="btn text-center btn-warning close-championship" data-sport="{{ sport.id }}">
												<i class="fas fa-exclamation-triangle"></i> Cerrar campeonato
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
	{/* {% if person.is_admin %} */}
	<div class="tab-pane fade" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-10 col-12 mt-5 offset-md-1">
					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create-modal"
						id="create-event-btn">
						Nuevo Evento
					</button>
				</div>
			</div>
			<div class="row">
				<div class="table-responsive col-md-10 offset-md-1 mt-4">
					<table id="dt-events" class="table table-striped table-bordered table-hover" cellspacing="0"
						width="100%">
						<thead>
							<tr>
								<th>Nombre</th>
								<th>Año</th>
								<th>Acciones</th>
							</tr>
						</thead>
						<tbody>
							{/* {% for event in events %} */}
							<tr>
								<td> [EVENT] </td>
								<td> [YEAR] </td>
								<td class="text-center">
									<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
										{/* <button type="button" class="btn text-center btn-info"
											data-toggle="modal" data-target="#edit-modal">
											<i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i> Editar
										</button> */}
										<button type="button" class="btn text-center btn-danger delete-event-btn"
											data-toggle="modal" data-target="#delete-modal">
											<i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i> Borrar
										</button>
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
	<div class="tab-pane fade" id="nav-locations" role="tabpanel" aria-labelledby="nav-contact-tab">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-10 col-12 mt-5 offset-md-1">
					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create-modal"
						id="create-location-btn">
						Nuevo Lugar
					</button>
				</div>
			</div>
			<div class="row">
				<div class="table-responsive col-md-10 offset-md-1 mt-4">
					<table id="dt-places" class="table table-striped table-bordered table-hover" cellspacing="0"
						width="100%">
						<thead>
							<tr>
								<th>Nombre</th>
								<th>Dirección</th>
								<th>Organización</th>
								<th>Acciones</th>
							</tr>
						</thead>
						<tbody>
							{/* {% for location in locations %} */}
							<tr>
								<td>[LOCATION]</td>
								<td>[ADDRESS]</td>
								<td>[UNI]</td>
								<td class="text-center">
									<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
										<button type="button" class="btn text-center btn-info edit-location-btn"
											data-location="{{location.id}}">
											<i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i> Editar
										</button>
										<button type="button" class="btn text-center btn-danger delete-location-btn"
											data-toggle="modal" data-target="#delete-modal"
											data-location="{{location.id}}" data-name="{{location.name}}">
											<i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i> Borrar
										</button>
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
	<div class="tab-pane fade" id="nav-universities" role="tabpanel" aria-labelledby="nav-contact-tab">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-10 col-12 mt-5 offset-md-1">
					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create-modal"
						id="create-uni-btn">
						Nueva Organización
					</button>
				</div>
			</div>
			<div class="row">
				<div class="table-responsive col-md-10 offset-md-1 mt-4">
					<table id="dt-unis" class="table table-striped table-bordered table-hover" cellspacing="0"
						width="100%">
						<thead>
							<tr>
								<th>Nombre</th>
								<th>Siglas</th>
								<th>Ciudad</th>
								<th>Acciones</th>
							</tr>
						</thead>
						<tbody>
							{/* {% for uni in universities %} */}
							<tr>
								<td> [UNIVERSITY] </td>
								<td> [UNI] </td>
								<td> [CITY] </td>
								<td class="text-center">
									<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
										<button type="button" class="btn text-center btn-info edit-uni-btn"
											data-uni="{{ uni.id }}">
											<i class="fas fa-edit fa-sm pr-2" aria-hidden="true"></i> Editar
										</button>
										<button type="button" class="btn text-center btn-danger delete-uni-btn"
											data-toggle="modal" data-target="#delete-modal" data-uni="{{uni.id}}"
											data-name="{{uni.name}}">
											<i class="fas fa-trash fa-sm pr-2" aria-hidden="true"></i> Borrar
										</button>
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
	{/* {% endif %} */}
</div>
      </div>
    );
  }
  