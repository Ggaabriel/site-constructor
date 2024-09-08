export interface IUser {
  id: string;
}
/**
 * Класс для взаимодействия с Telegram
 */
class Telegram {
  private tg: any;

  constructor() {
    // @ts-expect-error unknown type used right now, later Telegram interface must be here
    this.tg = window.Telegram.WebApp;
  }

  /**
   * - Telegram пользователь, если приложение открыто в Telegram
   *- Стандартный пользователь (id = 0), иначе
   */
  get user(): IUser {
    const user: IUser = this.tg.initDataUnsafe.user;
    if (user && user.id) {
      return user;
    }
    return { id: "0" };
  }

  /**
   * - Уведомляет Telegram о готовности (ready)
   * - Раскраывает приложение на весь экран (expand)
   * - Добавляет подтверждение для закрытия (enableClosingConfirmation)
   */
  windowInitiate(): void {
    this.tg.ready();
    this.tg.expand();
    this.tg.enableClosingConfirmation();
  }
}

export const telegram = new Telegram();
