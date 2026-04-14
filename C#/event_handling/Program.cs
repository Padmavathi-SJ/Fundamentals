using System;

namespace EventHandling
{
    // A delegate is like a "contract" that says:
    // "Any methods that lokks like this can be attatched to my event"
    // This delegate says: methods must return void and take one int
    public delegate void MyEventHandler(int value);

    // the counter class (Event Producer)
    class Counter
    {
        //This is the event - it's like a list of methods to call
        public event MyEventHandler? OnThresholdReached;

        private int currentValue = 0;
        private int targetThreshold;

        // Constructor - runs when we create a new Counter
        public Counter(int threshold)
        {
            targetThreshold = threshold;
        }

        // This method increases the counter by 1
        public void AddOne()
        {
            currentValue++;
            Console.WriteLine($"Current count: {currentValue}");

            // check if we reached the target number(threshold)
            if(currentValue >= targetThreshold)
            {
                Console.WriteLine($"\n!!! Reached {targetThreshold} !!!");

                // This is where the event happens
                // We check if anyone is listening, then call them
                if (OnThresholdReached != null)
                {
                    OnThresholdReached(currentValue);  // Fire the event!
                }
            }
        }

        public void ResetCounter()
        {
            currentValue = 0;
            Console.WriteLine("Counter reset to 0");
        }
    }

    // EVENT RESPONDERS (Event Consumers)
    // These classes don't know about each other - they just respond to events

    class SoundMaker
    {
        public void MakeBeep(int value)
        {
            Console.WriteLine($" BEEP BEEP! Counter reached {value}!");
        }
    }

    class MessageWrite
    {
        public void WriteMessage(int value)
        {
            Console.WriteLine($" MESSAGE: You have reached number {value}!");
        }
    }

    class LightBlinker
    {
        public void BlinkLight(int value)
        {
            Console.WriteLine($" LIGHT BLINKING!!! Value is {value}!");
        }
    }

    class FileSaver
    {
        public void SaveFile(int value)
        {
            Console.WriteLine($" SAVING: Counter value  {value} saved to file!");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== I will count from 1 to 5.");
            Console.WriteLine("When count reach the threshold, Multiple actions will happen!\n");

            // create the counter (set to trigger at 5)
            Counter myCounter = new Counter(5);

            // Create the responders (things that will react)
            SoundMaker sound = new SoundMaker();
            MessageWrite message = new MessageWrite();
            LightBlinker light = new LightBlinker();
            FileSaver file = new FileSaver();

            // SUBSCRIBE: Tell the counter who to notify when event happens
            // like hey counter, call these methods when you reach

            myCounter.OnThresholdReached += sound.MakeBeep;
            myCounter.OnThresholdReached += message.WriteMessage;
            myCounter.OnThresholdReached += light.BlinkLight;
            myCounter.OnThresholdReached += file.SaveFile;

            for (int i = 0; i <= 6; i++)
            {
                myCounter.AddOne(); // This will automatically trigger event at 5
            }

            // Unscubscribe: Remove one responder
            myCounter.OnThresholdReached -= sound.MakeBeep;

            // Reset counter and count again
            myCounter.ResetCounter();

            Console.WriteLine("\n Counting again from 1 to 5 (but no beep sound this time.)");

            for(int i=0; i<=5; i++)
            {
                myCounter.AddOne();
            }

            Console.WriteLine("Notice how events let us add or remvove responders without changing the Counter class!");

        }
    }

}