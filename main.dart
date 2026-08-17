import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
void main()=>runApp(const App());
class App extends StatelessWidget{const App({super.key});@override Widget build(BuildContext c)=>MaterialApp(debugShowCheckedModeBanner:false,title:'Varant Direction AI',theme:ThemeData(brightness:Brightness.dark,useMaterial3:true,colorSchemeSeed:Colors.blue),home:const HomeScreen());}
