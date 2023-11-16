import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';

class LandingDashboard extends StatefulWidget {
  const LandingDashboard({Key? key}) : super(key: key);

  @override
  _LandingDashboardState createState() => _LandingDashboardState();
}

class _LandingDashboardState extends State<LandingDashboard> {
  int _currentIndex = 0;

  List<String> imageList = [
    'assets/image1.jpg',
    'assets/image2.jpg',
    'assets/image3.jpg',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Text(
                'Drawer Header',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              title: const Text('Profile'),
              onTap: () {
                // Add functionality for Item 1
              },
            ),
            ListTile(
              title: const Text('Settings'),
              onTap: () {
                // Add functionality for Item 2
              },
            ),
            // Add more items as needed
          ],
        ),
      ),
      body: Container(
        padding: const EdgeInsets.all(16.0),
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/placeholder_image.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        
        child: Column(
          children: [
            const Text("Laham Hotels",style: TextStyle(fontSize: 40,fontWeight: FontWeight.bold,color: Colors.white),),
            const SizedBox(height: 20),
            CarouselSlider(
              options: CarouselOptions(
                height: 200.0,
                autoPlay: true,
                enlargeCenterPage: true,
                aspectRatio: 2.0,
                onPageChanged: (index, reason) {
                  setState(() {
                    _currentIndex = index;
                  });
                },
              ),
              items: imageList.map((imageUrl) {
                return Builder(
                  builder: (BuildContext context) {
                    return Container(
                      width: MediaQuery.of(context).size.width,
                      margin: const EdgeInsets.symmetric(horizontal: 5.0),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10.0),
                        image: DecorationImage(
                          image: AssetImage(imageUrl),
                          fit: BoxFit.cover,
                        ),
                      ),
                    );
                  },
                );
              }).toList(),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: GridView.count(
                crossAxisCount: 3,
                children: [
                  _buildDashboardItem(context, 'Page 1', Colors.blue, '/page1'),
                  _buildDashboardItem(context, 'Page 2', Colors.green, '/page2'),
                  _buildDashboardItem(context, 'Page 3', Colors.orange, '/page3'),
                  _buildDashboardItem(context, 'Page 4', Colors.red, '/page4'),
                  _buildDashboardItem(context, 'Page 5', Colors.purple, '/page5'),
                  _buildDashboardItem(context, 'Page 6', Colors.teal, '/page6'),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Search',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  Widget _buildDashboardItem(
      BuildContext context, String title, Color color, String route) {
    return GestureDetector(
      onTap: () {
        Navigator.pushNamed(context, route);
      },
      child: Card(
        elevation: 5.0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15.0),
        ),
        child: Container(
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(15.0),
          ),
          child: Center(
            child: Text(
              title,
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ),
    );
  }
}
