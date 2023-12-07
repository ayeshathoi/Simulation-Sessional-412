#include<bits/stdc++.h>
using namespace std;

#include "lcgrand.h"

#define num_events 2 //arrival, departure
#define BUSY 1
#define IDLE 0

ofstream event_orders("event_orders.txt");
ofstream result("result.txt");

float expon(float mean)
{
    return -mean * log(lcgrand(1));
}

//initialization variables
float simulation_time,total_delays, area_num_in_queue, area_server_status;
int server_state, num_customer_in_queue, num_customer_delayed;
float next_arrival_time, next_departure_time;
float mean_interarrival_time, mean_service_time, total_delays_required;
int total_event;
//arrival variables
queue<float> arrival;
int next_event_type; // 1 for arrival, 2 for departure
//timing variables
int arriver_customer = 0 , depart_customer = 0;
float last_event_time = 0.0;

void initialize()
{
    simulation_time = 0.0;
    server_state = IDLE;
    num_customer_in_queue = 0;
    num_customer_delayed = 0;
    total_delays = 0.0;
    area_num_in_queue = 0.0;
    area_server_status = 0.0;
    next_arrival_time = simulation_time + expon(mean_interarrival_time);
    next_departure_time = 1.0e+30;
    total_event = 0;
}


void timing()
{
    total_event++;
    float event_time_min = 1.0e+29; // to avoid infinite loop in timing function
    next_event_type = 0; // no event initially

    if (next_arrival_time <= next_departure_time)
    {
        event_time_min = next_arrival_time;
        next_event_type = 1; // arrival
        arriver_customer++;
        // print the event type with customer number
        event_orders<< total_event << ". Next event: Customer " << arriver_customer << " Arrival" << endl;
    }

    else
    {
        event_time_min = next_departure_time;
        next_event_type = 2; // departure
        depart_customer++;
        // print the event type with customer number
        event_orders<< total_event << ". Next event: Customer " << depart_customer << " Departure" << endl;
    }


    simulation_time = event_time_min; // advance the clock
}



void arrive()
{
    next_arrival_time = simulation_time + expon(mean_interarrival_time); // schedule next arrival

    if(server_state == BUSY)
    {
        num_customer_in_queue++;
        arrival.push(simulation_time); // add the customer to queue_list      
    }

    else
    {
        server_state = BUSY;
        // no queue_list update as no customer in queue
        num_customer_delayed++; // update number of customer served as the next customer went to server
        // print number_customer_served with customer number
        event_orders << "\n---------No. of customers delayed: "<< num_customer_delayed << "--------\n" <<endl;
        next_departure_time = simulation_time + expon(mean_service_time); // schedule next departure
    }
}


void depart()
{
    float delay;
    if(num_customer_in_queue == 0)
    {
        server_state = IDLE;
        next_departure_time = 1.0e+30; // to avoid infinite loop in timing function
    }

    else
    {
        num_customer_in_queue--; // as one customer left the queue to server
        // delete arrival element 1st element
        delay = simulation_time - arrival.front();
        arrival.pop();

        total_delays += delay ; // calculate delay
        num_customer_delayed++; // update number of customer served as the next customer went to server
        // print number_customer_served with customer number
        event_orders << "\n---------No. of customers delayed: "<< num_customer_delayed << "--------\n" <<endl;

        next_departure_time = simulation_time + expon(mean_service_time); // schedule next departure
    }

}

void report()
{
    //set precision
    result<<fixed<<setprecision(6);
    result<<"----Single-Server Queueing System----\n"<<endl;
    result<<"Mean inter-arrival time: "<<mean_interarrival_time<<" minutes" <<endl;
    result<<"Mean service time: "<<mean_service_time<<" minutes" <<endl;
    result<<"Number of customers: "<<int(total_delays_required)<<"\n"<<endl;

    result<<"Avg delay in queue: "<<total_delays/num_customer_delayed<<" minutes" <<endl; //not okay
    result<<"Avg number in queue: "<<area_num_in_queue/simulation_time<<endl; //okay
    result<<"Server utilization: "<<area_server_status/simulation_time <<endl; //okay
    result<<"Time simulation ended: "<<simulation_time<<" minutes" <<endl; //okay

}

void update_time_avg_stats()
{
    float time_since_last_event;
    time_since_last_event = simulation_time - last_event_time;
    last_event_time = simulation_time;

    area_num_in_queue += num_customer_in_queue * time_since_last_event;
    area_server_status += server_state * time_since_last_event;
}


int main()
{
    ifstream fin("in.txt");
    fin>>mean_interarrival_time>>mean_service_time>>total_delays_required;
    fin.close();

        initialize();

    while (num_customer_delayed < total_delays_required)
    {
        timing();
        update_time_avg_stats();
        if(next_event_type == 1)
        {
            arrive();
        }
        else if(next_event_type == 2)
        {
            depart();
        }
    }

    
   
    report();


}