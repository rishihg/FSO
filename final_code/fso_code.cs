using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NewFocus.Picomotor;
using System.IO.Ports;
using System.Threading;


namespace NewFocus.Picomotor
{
    class RelativeMove
    {
        static SerialPort _serialPort;
        static void Main(string[] args)
        {
            string[] Value1;
            int[] steps;

            _serialPort = new SerialPort();
            _serialPort.PortName = "COM8";//Set your board COM
            _serialPort.BaudRate = 9600;
            _serialPort.Open();

            Console.WriteLine("Waiting for device discovery...");
            string strDeviceKey = string.Empty;
            CmdLib8742 cmdLib = new CmdLib8742(false, 1000, ref strDeviceKey);
            Console.WriteLine("First Device Key = {0}", strDeviceKey);
            // If no devices were discovered
            if (strDeviceKey == null)
            {
                Console.WriteLine("No devices discovered.");
            }
            
            else
            {
                if (cmdLib.Open(strDeviceKey))
                {
                    for (int i = 1; i <= 4; i++)
                    {
                        cmdLib.SetAcceleration(strDeviceKey, i, 32000);
                        cmdLib.SetVelocity(strDeviceKey, i, 1500);
                        cmdLib.SaveToMemory(strDeviceKey);
                    }
                }
            }
            Console.WriteLine("Number of motors: ");
            string m = Console.ReadLine();
            while (true)
            {
                string oneLine = _serialPort.ReadLine().Trim();
                Value1 = oneLine.Split(',');
                steps = new int[Value1.Length];
                double[] values = new double[Value1.Length];
                bool flag = false;
                try
                {
                    for (int i = 0; i < Value1.Length; i++)
                    {
                        values[i] = Convert.ToDouble(Value1[i]);
                    }

                }
                catch (Exception ex)
                {
                    flag = true;
                    Console.WriteLine("error");
                }
                //oneLine != "" && !oneLine.Contains("\0") &&
                if (flag == false)
                {
                    if (Value1.Length == Convert.ToDouble(m))
                    {
                        //for (int i = 0; i < Value1.Length; i++)
                        //{
                        //    values[i] = Convert.ToDouble(Value1[i]);
                        //}
                        Console.WriteLine(oneLine);

                        int range = 200;

                        for (int i = 0; i < values.Length; i++)
                        {
                            steps[i] = (int)((2 * range * values[i]) / 1023 - range);
                            Console.WriteLine(steps[i]);
                        }
                    }
                    if (cmdLib.Open(strDeviceKey) && Value1.Length == Convert.ToDouble(m))
                    {

                        int i = 0;
                        switch (i)
                        {
                            case 0:
                                cmdLib.RelativeMove(strDeviceKey, i + 1, steps[i]);
                                bool isMotionDone1 = false;
                                bool a1 = cmdLib.GetMotionDone(strDeviceKey, i + 1, ref isMotionDone1);
                                Console.WriteLine(a1 + " M1");
                                i = i + 1;
                                Thread.Sleep(200);
                                if (Convert.ToDouble(m) == 1)
                                {
                                    continue;
                                }
                                else
                                {
                                    goto case 1;
                                }

                            case 1:
                                cmdLib.RelativeMove(strDeviceKey, i + 1, steps[i]);
                                bool isMotionDone2 = false;
                                bool a2 = cmdLib.GetMotionDone(strDeviceKey, i + 1, ref isMotionDone2);
                                Console.WriteLine(a2+" M2");
                                Thread.Sleep(200);
                                i = i + 1;
                                if (Convert.ToDouble(m) == 2)
                                {
                                    continue;
                                }
                                else
                                {
                                    goto case 2;
                                }

                            case 2:
                                cmdLib.RelativeMove(strDeviceKey, i + 1, steps[i]);
                                bool isMotionDone3 = false;
                                bool a3 = cmdLib.GetMotionDone(strDeviceKey, i + 1, ref isMotionDone3);
                                Console.WriteLine(a3+" M3");
                                i = i + 1;
                                Thread.Sleep(200);
                                if (Convert.ToDouble(m) == 3)
                                {
                                    continue;
                                }
                                else
                                {
                                    goto case 3;
                                }

                            case 3:
                                cmdLib.RelativeMove(strDeviceKey, i + 1, steps[i]);
                                bool isMotionDone4 = false;
                                bool a4 = cmdLib.GetMotionDone(strDeviceKey, i + 1, ref isMotionDone4);
                                Console.WriteLine(a4+" M4");
                                i = i + 1;
                                Thread.Sleep(200);
                                if (Convert.ToDouble(m) == 4)
                                {
                                    continue;
                                }
                                else
                                {
                                    continue;
                                }

                           default:
                                break;

                                //cmdLib.RelativeMove(strDeviceKey, i + 1, steps[i]);
                                //bool isMotionDone = false;
                                //bool a = cmdLib.GetMotionDone(strDeviceKey, i + 1, ref isMotionDone);
                                //Console.WriteLine(a);



                        }
                    }

                }
                //Console.WriteLine("Shutting down.");
                //cmdLib.Shutdown();

                //System.Threading.Thread.Sleep(200);
            }




        }





        // If the device was opened
        //
        //{
        //    int nMotor = 1;
        //    int nPosition = 0;

        //    // Set the current position to zero
        //    bool bStatus = cmdLib.SetZeroPosition(strDeviceKey, nMotor);

        //    if (!bStatus)
        //    {
        //        Console.WriteLine("I/O Error:  Could not set the current position.");
        //    }

        //    // Get the current position
        //    bStatus = cmdLib.GetPosition(strDeviceKey, nMotor, ref nPosition);

        //    if (!bStatus)
        //    {
        //        Console.WriteLine("I/O Error:  Could not get the current position.");
        //    }
        //    else
        //    {
        //        Console.WriteLine("Start Position = {0}", nPosition);
        //    }

        //    Console.WriteLine("Enter the relative steps to move (0 or Ctrl-C for no movement): ");
        //    string strInput = Console.ReadLine();
        //    int nSteps = Convert.ToInt32(strInput);

        //    if (nSteps != 0)
        //    {
        //        // Perform a relative move
        //        bStatus = cmdLib.RelativeMove(strDeviceKey, nMotor, nSteps);

        //        if (!bStatus)
        //        {
        //            Console.WriteLine("I/O Error:  Could not perform relative move.");
        //        }
        //    }

        //    bool bIsMotionDone = false;

        //    while (bStatus && !bIsMotionDone)
        //    {
        //        // Check for any device error messages
        //        string strErrMsg = string.Empty;
        //        bStatus = cmdLib.GetErrorMsg(strDeviceKey, ref strErrMsg);

        //        if (!bStatus)
        //        {
        //            Console.WriteLine("I/O Error:  Could not get error status.");
        //        }
        //        else
        //        {
        //            string[] strTokens = strErrMsg.Split(new string[] { ", " }, StringSplitOptions.RemoveEmptyEntries);

        //            // If the error message number is not zero
        //            if (strTokens[0] != "0")
        //            {
        //                Console.WriteLine("Device Error:  {0}", strErrMsg);
        //                break;
        //            }

        //            // Get the motion done status
        //            bStatus = cmdLib.GetMotionDone(strDeviceKey, nMotor, ref bIsMotionDone);

        //            if (!bStatus)
        //            {
        //                Console.WriteLine("I/O Error:  Could not get motion done status.");
        //            }
        //            else
        //            {
        //                // Get the current position
        //                bStatus = cmdLib.GetPosition(strDeviceKey, nMotor, ref nPosition);

        //                if (!bStatus)
        //                {
        //                    Console.WriteLine("I/O Error:  Could not get the current position.");
        //                }
        //                else
        //                {
        //                    Console.WriteLine("Position = {0}", nPosition);
        //                }
        //            }
        //        }
        //    }

        //    // Close the device
        //    cmdLib.Close(strDeviceKey);
        //}
    }

    // Shut down device communication


}




