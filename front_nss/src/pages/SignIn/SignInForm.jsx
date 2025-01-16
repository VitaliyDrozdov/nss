import React, { useContext } from "react";
import { useNavigate } from 'react-router-dom';

import { Box, Button, IconButton, TextField, useTheme } from "@mui/material";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";

import { Formik } from "formik";
import * as yup from "yup";

import { ColorModeContext } from "../../hooks/useTheme";
import { useAuth } from "../../hooks/useAuth"; 

const SignInForm = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const  { login } = useAuth();
  const navigate = useNavigate();

  const handleFormSubmit = (values) => {
    const address = 'http://localhost:5000/api/auth/login';
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(values)
    }

    fetch(address, params)
      .then(response => {
          if (response.status === 200) {
              login();
              navigate("/quoteOsago");
          }
          else if (response.status === 500) {
            throw new Error("Сервер недоступен");
          }
        console.log("start parsing data")
        return response.json()
      })
      .catch(error => {
        console.log(error.message)
      });
  };

  return (
    <>
    <Formik
      onSubmit={handleFormSubmit}
      initialValues={initialValues}
      validationSchema={checkoutSchema}
    >
      {({
        values,
        errors,
        touched,
        handleBlur,
        handleChange,
        handleSubmit,
      }) => (
        <form onSubmit={handleSubmit}>
          <Box
            display="flex"
            flexDirection="column"
            minWidth="420px"
            gap={3}
          >
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Введите email"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.username}
              name="username"
              error={!!touched.username && !!errors.username}
              helperText={touched.username && errors.username}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Введите пароль"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.contact}
              name="password"
              error={!!touched.password && !!errors.password}
              helperText={touched.password && errors.password}
            />
          </Box>
          <Box display="flex" justifyContent="space-between" mt={2}>
            <IconButton onClick={colorMode.toggleColorMode}>
              {theme.palette.mode === "dark" ? (
                <DarkModeOutlinedIcon />
              ) : (
                <LightModeOutlinedIcon />
              )}
            </IconButton>
            <Box>
              
              <Button type="submit" color="secondary" variant="contained">
                Войти
              </Button>
            </Box>
          </Box>
        </form>
      )}
    </Formik>

    <Box>
      <a href="/signup">Восстановить пароль</a>
    </Box>

    </>
  );
};

const checkoutSchema = yup.object().shape({
  username:      yup.string().required("обязательное!"),
  password:   yup.string().required("обязательное!"),
});

const initialValues = {
  username: "",
  password: "",
};

export default SignInForm;
