import TeamsSidebar from "components/sidebar/TeamsSidebar";
import TeamsTable from "components/table/TeamsTable";
import TableSearchPage from "./wrapper/TableSearchPage";

export default function Teams() {
  return (
    <TableSearchPage
      SidebarComponent={TeamsSidebar}
      TableComponent={TeamsTable}
      apiUrl="/api/teams/"
      label="equipos"
    />
  );
}
