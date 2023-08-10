using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BrightnessController.Abstractions;
using BrightnessController.Infrastructure;
using DryIoc;
using DryIoc.Microsoft.DependencyInjection;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;

namespace BrightnessController
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            Log.Logger = new LoggerConfiguration()
                .WriteTo.Console()
                .CreateBootstrapLogger();
            string token = "";
            bool isDebug = false;
            if(args.Length >= 2) 
            {
                var argList = args.ToList();
                var tokenIdx = argList.IndexOf("--token");
                if (tokenIdx >= 0)
                {
                    Log.Information("Token passed");
                    token = args[tokenIdx+1];
                }
                else
                {
                    tokenIdx = argList.IndexOf("-t");
                    if (tokenIdx >= 0)
                    {
                        Log.Information("Token passed");
                        token = args[tokenIdx+1];
                    }
                    else
                    {
                        Log.Error("No valid arguments parsed");
                        Log.Information("Valid Arguments are:");
                        Log.Information("-t|--token\tTo pass an Authtoken");
                        Log.Information($"Passed Arguments: {string.Join('|', args)}");
                    }
                }

                isDebug = args.Any(arg => arg == "--debug");
            }  
            else
            {
                Log.Warning("No Arguments passed");
            }

            var host = new HostBuilder()
                .ConfigureWebHostDefaults((builder) =>
                {
                    builder.UseStartup<Startup>();

                })
                .ConfigureServices((ctx, services) =>
                {
                    ctx.Configuration["AuthToken"] = token;
                    ctx.Configuration["IsDebug"] = isDebug.ToString();
                })
                .UseSerilog()
                .Build();
            await host.RunAsync();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}