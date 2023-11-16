import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_setup/chat_screen.dart';
import 'package:firebase_setup/constants.dart';
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  static String id = "login_screen";

  const LoginScreen({super.key});

  @override
  LoginScreenState createState() => LoginScreenState();
}

class LoginScreenState extends State<LoginScreen> {
  bool showSpinner = false;
  String email = '';
  String password = '';
  final _auth = FirebaseAuth.instance;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Center(
            child: DefaultTextStyle(
                style: TextStyle(
                  fontSize: 40.0,
                  fontWeight: FontWeight.w900,
                  color: Colors.black54,
                ),
             child:Text(
                ("Login Form"),
                textAlign: TextAlign.center, 
             ),
            ),
            ),
            const SizedBox(
              height: 48.0,
            ),
            TextField(
              textAlign: TextAlign.center,
              keyboardType: TextInputType.emailAddress,
              onChanged: (value) {
                email = value;
              },
              decoration:
                  kTextFieldDecoration.copyWith(hintText: 'Enter your email '),
            ),
            const SizedBox(
              height: 18.0,
            ),
            TextField(
              textAlign: TextAlign.center,
              obscureText: true,
              onChanged: (value) {
                password = value;
              },
              decoration: kTextFieldDecoration.copyWith(
                  hintText: 'Enter your password '),
            ),
            const SizedBox(
              height: 24.0,
            ),
            ElevatedButton(
                child: const Text('Log in'),
                onPressed: () async {
                  setState(() {
                    showSpinner = true;
                  });
                  //Login to existing account
                  try {
                    await _auth
                        .signInWithEmailAndPassword(
                            email: email, password: password)
                        .then((value) {
                      setState(() {
                        showSpinner = false;
                      });
                      Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) => const LandingDashboard()));
                    });
                    print('Successfully Login');
                  } catch (e) {
                    print(e);
                  }
                }),
          ],
        ),
      ),
    );
  }
}
