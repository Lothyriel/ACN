import asyncio
import os
import traceback

import selenium.common.exceptions as ex
from discord.ext import commands
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from src import Controlador


def roda_drive(custom_options=webdriver.ChromeOptions()):
    return webdriver.Chrome(ChromeDriverManager().install(), options=custom_options)


async def loga_metamask(driver):
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    explicit_wait = WebDriverWait(driver, 15)
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div/button").is_displayed())
        botao_iniciar = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div/button")
        botao_iniciar.click()

        await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button").is_displayed())
        botao_importar = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button")
        botao_importar.click()

        await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[2]").is_displayed())
        botao_concordo = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[2]")
        botao_concordo.click()

        await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/form/div[4]/div[1]/div/input").is_displayed())
        text_frase_chave = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/form/div[4]/div[1]/div/input")
        text_frase_chave.click()
        text_frase_chave.send_keys(os.getenv("FRASE_METAMASK"))

        nova_senha = "12345678"
        botao_nova_senha = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/form/div[5]/div/input")
        botao_nova_senha.click()
        botao_nova_senha.send_keys(nova_senha)

        botao_confirma_nova_senha = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/form/div[6]/div/input")
        botao_confirma_nova_senha.click()
        botao_confirma_nova_senha.send_keys(nova_senha)

        botao_aceita_contrato = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/form/div[7]/div")
        botao_aceita_contrato.click()

        botao_login = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/form/button")
        botao_login.click()

        await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[3]/div/div/button").is_displayed())

    except ex.NoSuchElementException:
        print(traceback.format_exc())


class Navegador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Controlador = bot.Controlador

    @commands.command(help="!cc <usuario> <mentira a ser enviada>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cc(self, ctx, usuario, *arg):
        driver = roda_drive()
        driver.get("https://curiouscat.qa/{}".format(usuario))
        explicit_wait = WebDriverWait(driver, 15)
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, explicit_wait.until,
                                       lambda d: driver.find_element(By.CLASS_NAME, u"css-11aywtz").is_displayed())

            campo_pergunta = driver.find_element(By.CLASS_NAME, "css-11aywtz")
            campo_pergunta.click()
            pergunta = " ".join(arg)
            campo_pergunta.send_keys(pergunta)
            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "//*[@class='css-1dbjc4n r-1a9ljyw r-z2wwpe r-1loqt21 r-atwnbb r-1otgn73 r-1i6wzkk r-lrvibr']").is_displayed())
            botao_enviar = driver.find_element(By.XPATH,
                                               "//*[@class='css-1dbjc4n r-1a9ljyw r-z2wwpe r-1loqt21 r-atwnbb r-1otgn73 r-1i6wzkk r-lrvibr']")
            botao_enviar.click()

            await ctx.send(ctx.author.mention + "Mentiras Espalhadas!!!")
        except ex.NoSuchElementException:
            print(traceback.format_exc())
        finally:
            driver.close()


async def get_novo_token():
    async def aceita_contrato():
        explicit_wait = WebDriverWait(driver, 15)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, driver.get, "https://marketplace.plantvsundead.com/farm#/login")

        try:
            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "/html/body/div/div/div/div[2]/div/div[2]/div[1]").is_displayed())

            botao_login_metamask = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div[2]/div[1]")
            botao_login_metamask.click()

            await loop.run_in_executor(None, explicit_wait.until, lambda d: len(driver.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])

            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "/html/body/div[1]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]").is_displayed())
            botao_proximo = driver.find_element(By.XPATH,
                                                "/html/body/div[1]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]")
            botao_proximo.click()

            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]").is_displayed())
            botao_conectar = driver.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]")
            botao_conectar.click()

            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "/html/body/div[1]/div/div[3]/div/div[3]/button[2]").is_displayed())
            botao_assinar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/button[2]")
            botao_assinar.click()

            driver.switch_to.window(driver.window_handles[0])
            await loop.run_in_executor(None, explicit_wait.until, lambda d: driver.find_element(By.XPATH,
                                                                                                "/html/body/div/div/div/div[1]/div[1]/nav/div[2]/div[1]/img").is_displayed())

        except ex.NoSuchElementException:
            print(traceback.format_exc())

    options = webdriver.ChromeOptions()
    options.add_extension("utils/metamask.crx")

    driver = roda_drive(options)
    await loga_metamask(driver)
    await aceita_contrato()
    await asyncio.sleep(1)
    driver.execute_script("alert (localStorage.getItem('token'));")

    Controlador.set_key("BEARER_TOKEN", driver.switch_to.alert.text)

    driver.quit()
