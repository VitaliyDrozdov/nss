import React, { useContext } from "react";
import { Link, useNavigate } from 'react-router-dom';

import { Box, Button, IconButton, TextField, useTheme } from "@mui/material";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";

import { Formik } from "formik";
import * as yup from "yup";

import { ColorModeContext } from "../../hooks/useTheme";

const SignUpForm = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const navigate = useNavigate();
  const handleFormSubmit = (values) => {
      const address = 'http://localhost:5000/api/auth/register';
      const params = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(values)
      }
  
      fetch(address, params)
        .then(response => {
            if (response.status === 201) {
                navigate("/signin");
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
            display="grid"
            gap={3}
            gridTemplateColumns="repeat(4, minmax(0, 1fr))"
          >
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Имя"
              onBlur={handleBlur}
              onChange={handleChange}
              //value={values.firstName}
              name="firstName"
              error={!!touched.firstName && !!errors.firstName}
              helperText={touched.firstName && errors.firstName}
              sx={{ gridColumn: "span 2" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Фамилия"
              onBlur={handleBlur}
              onChange={handleChange}
              //value={values.lastName}*
              name="lastName"
              error={!!touched.lastName && !!errors.lastName}
              helperText={touched.lastName && errors.lastName}
              sx={{ gridColumn: "span 2" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Username"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.username}
              name="username"
              error={!!touched.username && !!errors.username}
              helperText={touched.username && errors.username}
              sx={{ gridColumn: "span 4" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Номер телефона"
              onBlur={handleBlur}
              onChange={handleChange}
              //value={values.contact}
              name="contact"
              error={!!touched.contact && !!errors.contact}
              helperText={touched.contact && errors.contact}
              sx={{ gridColumn: "span 4" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Пароль"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.password}
              name="password"
              error={!!touched.password && !!errors.password}
              helperText={touched.password && errors.password}
              sx={{ gridColumn: "span 4" }}
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
              <Button component={Link} to="/signin" color="warning" variant="contained" sx={{mr: 2}}>
                Войти
              </Button>
              <Button type="submit" color="secondary" variant="contained">
                Создать
              </Button>
            </Box>
          </Box>
        </form>
      )}
    </Formik>
  );
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const checkoutSchema = yup.object().shape({
  firstName:  yup.string(),
  lastName:   yup.string(),
  username:      yup.string().required("обязательное!"),
  contact: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid"),
});

const initialValues = {
  username: "",
  password: "",
};

export default SignUpForm;
