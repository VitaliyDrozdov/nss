import TestForm from "./TestForm";

import { Box } from "@mui/material";
import Header from "../../components/Header";

const Test = ()  => {

  return (
    <Box m="20px">
      <Header title="Отправить котировку" subtitle="Заполните представленную форму" />
      <TestForm />
    </Box>
  );
};

export default Test;

