import React from "react";

import { Box, Button, TextField } from "@mui/material";


import { Formik } from "formik";
import * as yup from "yup";

import api from "../../../utils/api";

const SignUpForm = () => {
  
  const handleFormSubmit = async (values) => {

    try {
      const response = await api.post("/auth/register", values);

      if (response.status === 201) {
        console.log("Регистрация прошла успешно");
      } else {
        console.log("Неожиданный статус ответа:", response.status);
      }
    } catch (error) {
      if (error.response && error.response.status === 500) {
        console.error("Сервер недоступен");
      } else {
        console.error("Произошла ошибка:", error.message);
      }
    }
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
              label="email"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.email}
              name="email"
              error={!!touched.email && !!errors.email}
              helperText={touched.email && errors.email}
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

            <Box>
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
  firstName: yup.string(),
  lastName: yup.string(),
  email: yup.string().required("обязательное!"),
  contact: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid"),
});

const initialValues = {
  email: "",
  password: "",
};

export default SignUpForm;