import bcrypt from 'bcryptjs';
import fetch from 'node-fetch';

export const handler = async (event) => {
  const { value, course_uri } = event;

  const bcrypt_hashed = bcrypt.hashSync(value, 10); 
  const payload = {
    banner: 'B00899622',
    result: bcrypt_hashed,
    arn: process.env.AWS_LAMBDA_FUNCTION_INVOKED_ARN, 
    action: 'bcrypt',
    value: value,
  };

  try {
    const response = await fetch(course_uri, {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'Content-Type': 'application/json' },
    });

    return {
      statusCode: response.status,
      body: JSON.stringify(await response.json()),
    };
  } catch (e) {
    return {
      statusCode: 400,
      body: JSON.stringify({ errorMessage: 'An error' + e.message + 'occurred.' }),
    };
  }
};
