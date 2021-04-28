import React from "react";
import _ from "lodash";
import { withStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import cowin18 from "./api/cowin18";
import CentersTable from "./CentersTable";

const styles = (theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
});

class App extends React.Component {
  state = {
    districts: [],
    districtsById: {},
    centers: {},
    selectedDistrict: "",
    selectedDistrictName: "",
  };

  async componentDidMount() {
    const resp = await cowin18.get("/centers/");
    const centers = resp.data.centers;
    const districts = resp.data.districts;
    this.setState({
      districts,
      districtsById: _.keyBy(districts, "id"),
      centers,
    });
  }

  handleDistrictSelection = (event) => {
    const districtId = event.target.value;
    this.setState({
      selectedDistrict: districtId,
      selectedDistrictName: this.state.districtsById?.[districtId]?.name,
    });
  };

  render() {
    const { classes } = this.props;

    return (
      <div>
        <FormControl className={classes.formControl}>
          <InputLabel id="city-selector-label">City</InputLabel>
          <Select
            labelId="city-selector-label"
            id="city-selector"
            value={this.state.selectedDistrict}
            onChange={this.handleDistrictSelection}
          >
            {this.state.districts.map((district) => (
              <MenuItem key={district.id} value={district.id}>
                {district.name}
              </MenuItem>
            ))}
          </Select>
          <FormHelperText>Select City</FormHelperText>
        </FormControl>
        <CentersTable
          data={
            this.state.centers?.[`DISTRICT_${this.state.selectedDistrict}`] ??
            []
          }
        />
      </div>
    );
  }
}

export default withStyles(styles)(App);
