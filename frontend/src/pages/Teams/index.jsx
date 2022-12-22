import TeamsSidebar from "pages/Teams/TeamsSidebar";
import TeamsTable from "pages/Teams/TeamsTable";
import TableSearchPage from "../wrapper/TableSearchPage";

export default function Teams() {
  return (
    <TableSearchPage
      SidebarComponent={TeamsSidebar}
      TableComponent={TeamsTable}
      apiName="teams"
      label="equipos"
    />
  );
}
