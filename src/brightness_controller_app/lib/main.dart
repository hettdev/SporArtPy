import 'dart:convert';

import 'package:flutter/material.dart';
import 'dart:developer';
import 'package:http/http.dart' as http;

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: "Brightness Controller",
        theme: ThemeData(
          appBarTheme: const AppBarTheme(
            backgroundColor: Colors.white,
            foregroundColor: Colors.black,
          ),
        ),
        home: Scaffold(
          appBar: AppBar(
            title: const Text('Brightness Controller'),
          ),
          body: const BrightnessSlider(),
        ));
  }
}

class BrightnessSlider extends StatefulWidget {
  const BrightnessSlider({Key? key}) : super(key: key);

  @override
  _BrightnessSliderState createState() => _BrightnessSliderState();
}

class _BrightnessSliderState extends State<BrightnessSlider> {
  double _sliderValue = 80;
  final _style = const TextStyle(fontSize: 18);
  bool _isTurnedOn = true;
  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: Column(
        children: [
          Container(
            margin: const EdgeInsets.only(top: 100),
          ),
          Container(
            margin: const EdgeInsets.all(18),
            child: Text(
              _sliderValue.round().toString(),
              style: _style,
            ),
          ),
          Container(
            margin: const EdgeInsets.all(18),
            child: Slider(
              value: _sliderValue,
              min: 0,
              max: 100,
              divisions: 100,
              label: _sliderValue.round().toString(),
              onChanged: (double val) {
                setState(() {
                  _sliderValue = val;
                  _isTurnedOn = true;
                });
              },
              onChangeEnd: (double val) {
                postNewValue(val.round());
              },
            ),
          ),
          Container(
            margin: const EdgeInsets.all(18),
            child: IconButton(
              icon: _isTurnedOn
                  ? const Icon(Icons.lightbulb)
                  : const Icon(Icons.lightbulb_outline),
              onPressed: () {
                setState(() {
                  _isTurnedOn = !_isTurnedOn;
                });
                if (_isTurnedOn) {
                  postNewValue(_sliderValue.round());
                } else {
                  postNewValue(0);
                }
              },
            ),
          ),
        ],
      ),
    );
  }

  Future<http.Response> postNewValue(val) async {
    try {
      var _body = jsonEncode(val);
      return await http.post(
        Uri.parse('http://192.168.178.14:5000/api/brightness/'),
        headers: <String, String>{
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: _body,
      );
    } on Exception catch (e) {
      log(e.toString());
      rethrow;
    }
  }

  Future<String> getBrightnessFromServer() async {
    try {
      var result = await http.get(
        Uri.parse('http://192.168.178.14:5000/api/brightness/'),
        headers: <String, String>{
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      return result.body;
    } on Exception catch (_) {
      return "Err";
    }
  }
}
