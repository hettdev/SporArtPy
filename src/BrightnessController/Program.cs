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
using Microsoft.Extensions.Logging;

namespace BrightnessController
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            string token = "";
            if(args.Length >= 2) 
            {
                if (args[0] == "--token" || args[0] == "-t")
                {
                    Console.WriteLine("Token passed");
                    token = args[1];
                }
                else
                {
                    Console.WriteLine("No valid arguments parsed");
                    Console.WriteLine("Valid Arguments are:");
                    Console.WriteLine("-t|--token\tTo pass an Authtoken");
                }
            }  
            else
            {
                Console.WriteLine("No Arguments passed");
            }

            var container = new Container();
            container.Register<ILocalStorage, LocalStorage>();
            
            var host = new HostBuilder()
                .ConfigureWebHostDefaults((builder) =>
                {
                    builder.UseStartup<Startup>();
                    
                })
                .ConfigureServices((ctx, services) =>
                {
                    ctx.Configuration["AuthToken"] = token;
                })
                .UseServiceProviderFactory(new DryIocServiceProviderFactory(container))
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
