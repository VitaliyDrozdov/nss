import QuoteOsagoForm from "./QuoteOsagoForm";

import { Box } from "@mui/material";
import Header from "../../components/Header";

const QuoteOsago = ()  => {

  return (
    <Box >
      <Header title="Отправить котировку" subtitle="Заполните представленную форму" />
      <QuoteOsagoForm />
    </Box>
  );
};

export default QuoteOsago;

