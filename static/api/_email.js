import nodemailer from 'nodemailer'

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false,
  auth: {
    user: process.env.SMTP_EMAIL || 'memogazar049@gmail.com',
    pass: process.env.SMTP_PASSWORD || '',
  },
})

export async function sendEmail(to, subject, html) {
  await transporter.sendMail({
    from: `"Zain Media" <${process.env.SMTP_EMAIL || 'memogazar049@gmail.com'}>`,
    to,
    subject,
    html,
  })
}
