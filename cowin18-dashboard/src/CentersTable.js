import React from "react";
import { DataGrid } from "@material-ui/data-grid";

class CentersTable extends React.Component {
  columns = [
    { field: "center_id", headerName: "Center ID", width: 150 },
    { field: "name", headerName: "Center Name", width: 400 },
    { field: "block_name", headerName: "Block Name", width: 250 },
    {
      field: "pincode",
      headerName: "Pincode",
      width: 150,
    },
    { field: "date", headerName: "Session Date", width: 250 },
    { field: "available_capacity", headerName: "Available Slots", width: 200 },
    { field: "vaccine", headerName: "Vaccine", width: 250 },
  ];

  render() {
    return (
      <div style={{ height: 600, width: "100%" }}>
        <DataGrid rows={this.props.data} columns={this.columns} pageSize={50} />
      </div>
    );
  }
}

export default CentersTable;
