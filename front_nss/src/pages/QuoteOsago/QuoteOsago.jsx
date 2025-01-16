import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import QuoteOsagoForm from "./QuoteOsagoForm";
import { Box } from "@mui/material";
import Header from "../../components/Header";

import { useAuth } from "../../hooks/useAuth";

const QuoteOsago = () => {
  
  const { isLoggedIn } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/signin");
    }
  }, [isLoggedIn, navigate]);

  if (!isLoggedIn) {
    return null;
  }

  return (
    <Box>
      <Header title="Отправить котировку" subtitle="Заполните представленную форму" />
      <QuoteOsagoForm />
    </Box>
  );
};

export default QuoteOsago;