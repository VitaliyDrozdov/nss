import React from 'react';
import { TextField, Button, Box, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { Formik, Form, FieldArray, ErrorMessage } from 'formik';
import * as Yup from 'yup';

//адрес вашего эндпоинта, который будет принимать запросы из формы
const address = 'http://localhost:5000/api/quote';


const initialValues = {
  quote: {
    header: {
      runId: '',
      quoteId: '',
      dateTime: new Date().toISOString(),
    },
    product: {
      productType: 'osago',
      productCode: '0',
    },
    subjects: [
      {
        firstName: '',
        secondName: '',
        middleName: '',
        birthDate: '',
        gender: '',
        addresses: [
          {
            country: '',
            region: '',
            city: '',
            street: '',
            houseNumber: '',
            apartmentNumber: '',
          },
        ],
        documents: [
          {
            documentType: '',
            documentNumber: '',
            issueDate: '',
          },
        ],
      },
    ],
  },
};



const Page = () => {
  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await fetch(address, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "quote": {
              "header": {
                  "runId": "123e4567-e89b-12d3-a456-426655440000",
                  "quoteId": "456",
                  "dateTime": "2024-04-12T13:52:26.509Z"
              },
              "product": {
                  "productType": "osago",
                  "productCode": "prod001"
              },
              "subjects": [
                  {
                      "firstName": "Алексей",
                      "secondName": "С",
                      "middleName": "Владимирович",
                      "birthDate": "1990-09-02",
                      "gender": "male",
                      "addresses": [
                          {
                              "country": "Россия",
                              "region": "Москва",
                              "city": "Москва",
                              "street": "Тверская",
                              "houseNumber": "1",
                              "apartmentNumber": "101"
                          }
                      ],
                      "documents": [
                          {
                              "documentType": "passport",
                              "documentNumber": "1234567890",
                              "issueDate": "2010-01-01"
                          }
                      ]
                  }
              ]
          }
      }
      )
      })
      .then(response => response.json())
      .then(data => console.log(data))
    } catch (error) {
      console.error('Error:', error);
    }
    setSubmitting(false);
  };
  
  

  return (
    <Formik
      initialValues={initialValues}
      
      onSubmit={handleSubmit}
    >
      {({ values, isSubmitting }) => (
        <Form>
          <TextField name="quote.header.runId" placeholder="Run ID" />
          <ErrorMessage name="quote.header.runId" component="div" />

          <TextField name="quote.header.quoteId" placeholder="Quote ID" />
          <ErrorMessage name="quote.header.quoteId" component="div" />

          <FieldArray name="quote.subjects">
            {({ push, remove }) => (
              <div>
                {values.quote.subjects.map((subject, index) => (
                  <div key={index}>
                    <h3>Subject {index + 1}</h3>
                    <TextField name={`quote.subjects.${index}.firstName`} placeholder="First Name" />
                    <ErrorMessage name={`quote.subjects.${index}.firstName`} component="div" />

                    <TextField name={`quote.subjects.${index}.secondName`} placeholder="Second Name" />
                    <ErrorMessage name={`quote.subjects.${index}.secondName`} component="div" />

                    <TextField name={`quote.subjects.${index}.middleName`} placeholder="Middle Name" />
                    <ErrorMessage name={`quote.subjects.${index}.middleName`} component="div" />

                    <TextField name={`quote.subjects.${index}.birthDate`} type="date" />
                    <ErrorMessage name={`quote.subjects.${index}.birthDate`} component="div" />

                    <FormControl variant="filled" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel>Gender</InputLabel>

                    <Select name={`quote.subjects.${index}.gender`} label="Gender">
                      <MenuItem value="male">Male</MenuItem>
                      <MenuItem value="female">Female</MenuItem>
                    </Select>
                    </FormControl>

                    <FieldArray name={`quote.subjects.${index}.addresses`}>
                      {({ push: pushAddress, remove: removeAddress }) => (
                        <div>
                          {subject.addresses.map((address, addressIndex) => (
                            <div key={addressIndex}>
                              <h4>Address {addressIndex + 1}</h4>
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.country`} placeholder="Country" />
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.region`} placeholder="Region" />
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.city`} placeholder="City" />
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.street`} placeholder="Street" />
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.houseNumber`} placeholder="House Number" />
                              <TextField name={`quote.subjects.${index}.addresses.${addressIndex}.apartmentNumber`} placeholder="Apartment Number" />
                              <Button type="button" onClick={() => removeAddress(addressIndex)}>Remove Address</Button>
                            </div>
                          ))}
                          <Button type="submit" color="secondary" variant="contained" onClick={() => pushAddress({ country: '', region: '', city: '', street: '', houseNumber: '', apartmentNumber: '' })}>
                            Add Address
                          </Button>
                        </div>
                      )}
                    </FieldArray>

                    <FieldArray name={`quote.subjects.${index}.documents`}>
                      {({ push: pushDocument, remove: removeDocument }) => (
                        <div>
                          {subject.documents.map((document, documentIndex) => (
                            <div key={documentIndex}>
                              <h4>Document {documentIndex + 1}</h4>
                              <TextField name={`quote.subjects.${index}.documents.${documentIndex}.documentType`} placeholder="Document Type" />
                              <TextField name={`quote.subjects.${index}.documents.${documentIndex}.documentNumber`} placeholder="Document Number" />
                              <TextField name={`quote.subjects.${index}.documents.${documentIndex}.issueDate`} type="date" />
                              <Button type="button" color="secondary" variant="contained" onClick={() => removeDocument(documentIndex)}>Remove Document</Button>
                            </div>
                          ))}
                          <Button type="button" color="secondary" variant="contained" onClick={() => pushDocument({ documentType: '', documentNumber: '', issueDate: '' })}>
                            Add Document
                          </Button>
                        </div>
                      )}
                    </FieldArray>
                    <Button type="button" color="secondary" variant="contained" onClick={() => remove(index)}>Remove Subject</Button>
                  </div>
                ))}
                <Button
                  type="button"
                  color="secondary"
                  variant="contained"
                  onClick={() => push({
                    firstName: '',
                    secondName: '',
                    middleName: '',
                    birthDate: '',
                    gender: '',
                    addresses: [],
                    documents: []
                  })}>
                  Add Subject
                </Button>
              </div>
            )}
          </FieldArray>

          <Box display="flex" justifyContent="end" mt="30px">
            <Button type="submit" color="third" variant="contained" disabled={isSubmitting}>
              Submit
            </Button>
          </Box>




        </Form>
      )}
    </Formik>
  );
};

export default Page;